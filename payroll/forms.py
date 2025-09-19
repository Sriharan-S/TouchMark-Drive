from django import forms
from .models import Salary, Attendance
import datetime

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
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    current_year = datetime.date.today().year
    YEAR_CHOICES = [(year, year) for year in range(current_year - 10, current_year + 2)]

    month = forms.ChoiceField(choices=MONTH_CHOICES, initial=datetime.date.today().month)
    year = forms.ChoiceField(choices=YEAR_CHOICES, initial=current_year)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'relative block w-full px-3 py-3 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
            })

class AttendanceForm(forms.Form):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    current_year = datetime.date.today().year
    YEAR_CHOICES = [(year, year) for year in range(current_year - 10, current_year + 2)]

    month = forms.ChoiceField(choices=MONTH_CHOICES, initial=datetime.date.today().month)
    year = forms.ChoiceField(choices=YEAR_CHOICES, initial=current_year)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'relative block w-full px-3 py-3 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'
            })