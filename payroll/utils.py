from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from num2words import num2words
from .models import Salary, Attendance

def generate_payslip_pdf(payroll):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(inch, height - inch, f"Payslip for {payroll.employee}")
    p.drawString(inch, height - 1.2 * inch, f"Month/Year: {payroll.month}/{payroll.year}")
    p.drawString(inch, height - 1.4 * inch, f"Employee Code: {payroll.employee.emp_code}")

    p.drawString(inch, height - 2 * inch, "Earnings")
    p.drawString(inch * 3, height - 2 * inch, "Amount")

    try:
        salary = Salary.objects.get(employee=payroll.employee)
    except Salary.DoesNotExist:
        # You might want to handle this case more gracefully
        # For now, we'll just return an empty PDF or a PDF with an error message.
        p.drawString(inch, height - inch, "Salary information not found for this employee.")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    basic_pay = salary.basic_pay
    hra = basic_pay * salary.hra_percentage / 100
    allowance = basic_pay * salary.allowance_percentage / 100

    p.drawString(inch, height - 2.2 * inch, "Basic Pay")
    p.drawString(inch * 3, height - 2.2 * inch, f"{basic_pay:.2f}")
    p.drawString(inch, height - 2.4 * inch, "HRA")
    p.drawString(inch * 3, height - 2.4 * inch, f"{hra:.2f}")
    p.drawString(inch, height - 2.6 * inch, "Allowance")
    p.drawString(inch * 3, height - 2.6 * inch, f"{allowance:.2f}")

    p.drawString(inch, height - 3 * inch, "Deductions")
    p.drawString(inch * 3, height - 3 * inch, "Amount")

    pf = payroll.gross_salary * salary.pf_percentage / 100
    tax = payroll.gross_salary * salary.tax_percentage / 100

    p.drawString(inch, height - 3.2 * inch, "Provident Fund")
    p.drawString(inch * 3, height - 3.2 * inch, f"{pf:.2f}")
    p.drawString(inch, height - 3.4 * inch, "Tax")
    p.drawString(inch * 3, height - 3.4 * inch, f"{tax:.2f}")

    # Fetch attendance details using employee, month, and year
    attendance = Attendance.objects.get(employee=payroll.employee, month=payroll.month, year=payroll.year)
    present_days = attendance.days_present
    absent_days = attendance.total_working_days - present_days

    # Add attendance details to the PDF
    p.drawString(inch, height - 1.6 * inch, f"Present Days: {present_days}")
    p.drawString(inch, height - 1.8 * inch, f"Absent Days: {absent_days}")

    p.drawString(inch, height - 3.6 * inch, "Absent Days Deduction")
    absent_days_deduction = (basic_pay / attendance.total_working_days) * absent_days
    p.drawString(inch * 3, height - 3.6 * inch, f"{absent_days_deduction:.2f}")

    # Update total deductions
    total_deductions = pf + tax + absent_days_deduction
    p.drawString(inch, height - 3.8 * inch, "Total Deductions")
    p.drawString(inch * 3, height - 3.8 * inch, f"{total_deductions:.2f}")

    p.drawString(inch, height - 4 * inch, f"Gross Salary: {payroll.gross_salary:.2f}")
    p.drawString(inch, height - 4.2 * inch, f"Total Deductions: {payroll.deductions:.2f}")
    p.drawString(inch, height - 4.4 * inch, f"Net Salary: {payroll.net_salary:.2f}")

    net_salary_words = num2words(payroll.net_salary, to='currency', lang='en_IN').replace('euro', 'rupees')
    p.drawString(inch, height - 4.8 * inch, f"In words: {net_salary_words}")


    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
