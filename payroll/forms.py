from django import forms
from .models import Salary

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['basic_pay', 'hra_percentage', 'allowance_percentage', 'pf_percentage', 'tax_percentage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'relative block w-full px-3 py-3 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
            })

class PayrollRunForm(forms.Form):
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField()
