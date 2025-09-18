from django import forms
from .models import Salary

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['basic_pay', 'hra_percentage', 'allowance_percentage', 'pf_percentage', 'tax_percentage']

class PayrollRunForm(forms.Form):
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField()

