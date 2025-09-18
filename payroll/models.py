from django.db import models
from employees.models import Employee

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    hra_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    allowance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Salary for {self.employee}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"Payroll for {self.employee} - {self.month}/{self.year}"

