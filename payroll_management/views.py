from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee

@login_required
def dashboard_view(request):
    active_employees = Employee.objects.filter(is_active=True).count()
    context = {
        'active_employees': active_employees
    }
    return render(request, 'dashboard.html', context)

