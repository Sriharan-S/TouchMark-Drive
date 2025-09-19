from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/<int:pk>/update/', views.salary_update, name='salary_update'),
    path('run/', views.payroll_run, name='payroll_run'),
    path('payslip/<int:payroll_id>/', views.view_payslip, name='view_payslip'),
    path('payslip/<int:payroll_id>/download/', views.download_payslip, name='download_payslip'),
    path('attendance/', views.attendance, name='attendance'),
]