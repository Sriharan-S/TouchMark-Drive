from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Salary, Payroll
from employees.models import Employee
from .forms import SalaryForm, PayrollRunForm
from .utils import generate_payslip_pdf

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
                    gross = salary.basic_pay + (salary.basic_pay * salary.hra_percentage / 100) + (salary.basic_pay * salary.allowance_percentage / 100)
                    deductions = (gross * salary.pf_percentage / 100) + (gross * salary.tax_percentage / 100)
                    net = gross - deductions

                    Payroll.objects.update_or_create(
                        employee=employee, month=month, year=year,
                        defaults={'gross_salary': gross, 'deductions': deductions, 'net_salary': net}
                    )
                except Salary.DoesNotExist:
                    messages.warning(request, f'Salary not set up for {employee}.')
            messages.success(request, 'Payroll run completed successfully.')
            return redirect('payroll:payroll_run')
    else:
        form = PayrollRunForm()

    payrolls = Payroll.objects.all().order_by('-year', '-month')
    return render(request, 'payroll/payroll_run.html', {'form': form, 'payrolls': payrolls})

@login_required
def view_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    return render(request, 'payroll/payslip.html', {'payroll': payroll})

@login_required
def download_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    pdf = generate_payslip_pdf(payroll)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payroll.employee.emp_code}_{payroll.month}_{payroll.year}.pdf"'
    return response

