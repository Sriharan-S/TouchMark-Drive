from django.db import models
from employees.models import Employee

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_details')
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hra_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="HRA %")
    allowance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Allowance %")
    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="PF %")
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Tax %")

    def __str__(self):
        return f"Salary for {self.employee.first_name} {self.employee.last_name}"


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payroll for {self.employee} - {self.month}/{self.year}"
