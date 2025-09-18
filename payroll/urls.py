from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('salary/<int:employee_id>/', views.salary_setup, name='salary_setup'),
    path('run/', views.payroll_run, name='payroll_run'),
    path('payslip/<int:payroll_id>/', views.view_payslip, name='view_payslip'),
    path('payslip/<int:payroll_id>/download/', views.download_payslip, name='download_payslip'),
]
