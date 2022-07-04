from django import forms
from django.utils import timezone

from .models import Employee
from .models import Contract
from .models import working_record
from .models import Post_Report
#from .models import TEST_Post_Report

#共通のフォーム
class log_in_form(forms.Form):
    ID=forms.CharField(label='ID')
    password=forms.CharField(label='Password')

#Employerのフォーム
class ID_form(forms.Form):
    Input_ID=forms.CharField(label='ID')

class employee_registration(forms.Form):
    name=forms.CharField(required=True)
    tax_category=forms.ChoiceField(required=True, choices=((1,"甲"), (2,"乙")))


class contract_registration(forms.Form):
    day_tuple=(
        (1, 'Sunday'),(2, 'Monday'), (3, 'Tuesday'),
        (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')
    )

    contract_start=forms.DateField(required=True, widget=forms.NumberInput(attrs={'type':'date'}))
    contract_end=forms.DateField(required=True, widget=forms.NumberInput(attrs={'type':'date'}))
    wage_per_hour=forms.IntegerField(required=True)
    job_description=forms.CharField(required=True)
    day_off=forms.ChoiceField(required=True, choices=day_tuple)


class change_password(forms.Form):
    current_pw=forms.CharField(label='CURRENT PASSWORD', widget=forms.PasswordInput)
    NEW_pw_01=forms.CharField(label='NEW PASSWORD', widget=forms.PasswordInput)
    NEW_ps_02=forms.CharField(label='NEW PASSWORD (AGAIN)', widget=forms.PasswordInput)
    #1

class see_contracts_form(forms.Form):
    basis_date=forms.DateField()


class jd_selection_form(forms.Form):
    job_description=forms.ChoiceField(choices=[])  

class comment_form(forms.ModelForm):
    class Meta:
        model=working_record
        fields=['comment']

class post_report_form(forms.Form):
    clock_in_or_out=forms.BooleanField(required=True, widget=forms.RadioSelect(choices=[(True,'IN'),(False,'OUT')]))
    date=forms.DateField(required=True, widget=forms.NumberInput(attrs={"type":"date"}))
    time=forms.TimeField(required=True)
    job_description=forms.ChoiceField(required=True, choices=[])
    comment=forms.CharField(required=False)


class select_year_month_form(forms.Form):
    year_and_month=forms.ChoiceField(choices=[])



