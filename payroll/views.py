from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Salary, Payroll, Attendance
from employees.models import Employee
from .forms import SalaryForm, PayrollRunForm, AttendanceForm
from .utils import generate_payslip_pdf
import datetime

@login_required
def salary_setup(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    try:
        salary = Salary.objects.get(employee=employee)
    except Salary.DoesNotExist:
        salary = None

    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = employee
            instance.save()
            messages.success(request, 'Salary details saved successfully.')
            return redirect('employees:employee_list')
    else:
        form = SalaryForm(instance=salary)

    return render(request, 'payroll/salary_setup.html', {'form': form, 'employee': employee})

@login_required
def salary_list(request):
    # Ensure a Salary object exists for every active employee
    active_employees = Employee.objects.filter(is_active=True)
    for employee in active_employees:
        Salary.objects.get_or_create(employee=employee)

    # Fetch all salary objects for active employees to display
    salaries = Salary.objects.filter(employee__is_active=True).select_related('employee')
    return render(request, 'payroll/salary_list.html', {'salaries': salaries})

@login_required
def salary_update(request, pk):
    salary = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary details updated successfully.')
            return redirect('payroll:salary_list')
    else:
        form = SalaryForm(instance=salary)

    return render(request, 'payroll/salary_form.html', {'form': form, 'salary': salary})

@login_required
def payroll_run(request):
    if request.method == 'POST':
        form = PayrollRunForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            employees = Employee.objects.filter(is_active=True)
            for employee in employees:
                try:
                    salary = Salary.objects.get(employee=employee)
                    attendance = Attendance.objects.get(employee=employee, month=month, year=year)

                    monthly_gross = salary.basic_pay + (salary.basic_pay * salary.hra_percentage / 100) + (salary.basic_pay * salary.allowance_percentage / 100)
                    earned_gross = (monthly_gross / attendance.total_working_days) * attendance.days_present

                    deductions = (earned_gross * salary.pf_percentage / 100) + (earned_gross * salary.tax_percentage / 100)
                    net = earned_gross - deductions

                    Payroll.objects.update_or_create(
                        employee=employee, month=month, year=year,
                        defaults={'gross_salary': earned_gross, 'deductions': deductions, 'net_salary': net}
                    )
                except Salary.DoesNotExist:
                    messages.warning(request, f'Salary not set up for {employee}.')
                except Attendance.DoesNotExist:
                    messages.error(request, f'Attendance not found for {employee} for {month}/{year}. Please mark attendance to proceed.')
                    return redirect('payroll:payroll_run')

            messages.success(request, 'Payroll run completed successfully.')
            return redirect('payroll:payroll_run')
    else:
        form = PayrollRunForm()

    payrolls = Payroll.objects.all().order_by('-year', '-month')
    return render(request, 'payroll/payroll_run.html', {'form': form, 'payrolls': payrolls})

@login_required
def view_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)

    try:
        salary = Salary.objects.get(employee=payroll.employee)
        attendance = Attendance.objects.get(employee=payroll.employee, month=payroll.month, year=payroll.year)
    except Salary.DoesNotExist:
        messages.error(request, f"Salary information not found for {payroll.employee}.")
        return redirect('payroll:payroll_run')
    except Attendance.DoesNotExist:
        messages.error(request, f"Attendance not found for {payroll.employee} for {payroll.month}/{payroll.year}.")
        return redirect('payroll:payroll_run')

    basic_pay = salary.basic_pay
    hra = basic_pay * salary.hra_percentage / 100
    allowance = basic_pay * salary.allowance_percentage / 100

    pf = payroll.gross_salary * salary.pf_percentage / 100
    tax = payroll.gross_salary * salary.tax_percentage / 100

    absent_days = attendance.total_working_days - attendance.days_present
    absent_days_deduction = (salary.basic_pay / attendance.total_working_days) * absent_days

    deductions = pf + tax + absent_days_deduction

    context = {
        'payroll': payroll,
        'hra': hra,
        'allowance': allowance,
        'pf': pf,
        'tax': tax,
        'attendance': attendance,
        'absent_days': absent_days,
        'absent_days_deduction': absent_days_deduction,
        'deductions': deductions,
        'salary': salary,  # Added salary object to context
    }
    return render(request, 'payroll/payslip.html', context)

@login_required
def download_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    pdf = generate_payslip_pdf(payroll)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payroll.employee.emp_code}_{payroll.month}_{payroll.year}.pdf"'
    return response

@login_required
def attendance(request):
    if request.method == 'POST' and 'fetch_employees' in request.POST:
        form = AttendanceForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            total_working_days = request.POST.get('total_working_days')
            employees = Employee.objects.filter(is_active=True)
            context = {
                'form': form,
                'employees': employees,
                'month': month,
                'year': year,
                'total_working_days': total_working_days,
            }
            return render(request, 'payroll/attendance.html', context)
    elif request.method == 'POST' and 'save_attendance' in request.POST:
        month = request.POST.get('month')
        year = request.POST.get('year')
        total_working_days = request.POST.get('total_working_days')
        employees = Employee.objects.filter(is_active=True)
        for employee in employees:
            days_present = request.POST.get(f'days_present_{employee.pk}')
            Attendance.objects.update_or_create(
                employee=employee,
                month=month,
                year=year,
                defaults={
                    'total_working_days': total_working_days,
                    'days_present': days_present,
                }
            )
        messages.success(request, 'Attendance saved successfully.')
        return redirect('payroll:attendance')
    else:
        form = AttendanceForm()
    return render(request, 'payroll/attendance.html', {'form': form})