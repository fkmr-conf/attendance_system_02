from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your models here.

class Employer(models.Model):
    IDcode=models.CharField(max_length=10, db_column='Employer_ID')

    name=models.CharField(max_length=30, db_column='Employer_name')
    log_in_password=models.CharField(max_length=100)
    def __str__(self):
        return 'ID:' + self.IDcode + ' NAME:' + self.name

class Employee(models.Model):
    tax_category_list=(
        (1, '甲'), (2, '乙')
    )
    IDcode=models.CharField(max_length=10, blank=True, db_column='Employee_ID')
    name=models.CharField(max_length=50, db_column='Employee_name')
    log_in_password=models.CharField(max_length=100, default='000')
    tax_category=models.IntegerField(choices=tax_category_list)
    
    def __str__(self):
        return 'ID:' + self.IDcode + '  NAME: ' + self.name

class Contract(models.Model):
    day_list=(
        (1, 'Sunday'),(2, 'Monday'), (3, 'Tuesday'),
        (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')
    )

    cnt_employee=models.CharField(max_length=10, blank=True, null=True)
    cnt_employer=models.CharField(max_length=10, default='未登録')
    #employee=models.ForeignKey(Employee, on_delete=models.CASCADE)#ここがだめか
    #employer_ID=models.ForeignKey(Employer, on_delete=models.CASCADE,default='未登録')#ここがだめか
    contract_start=models.DateField()
    contract_end=models.DateField()
    wage_per_hour=models.IntegerField(default=1000)
    job_description=models.CharField(max_length=100)
    day_off=models.IntegerField(choices=day_list)#ここで設定せずとも？

class working_record(models.Model):
    employee_ID=models.CharField(max_length=10, blank=True)
    #date_and_time=models.DateTimeField()
    date=models.DateField()
    time=models.TimeField()
    clock_in_or_out=models.BooleanField()#True='clock_in' False='clock_out'
    job_description=models.CharField(max_length=100, blank=True, null=True) #出勤のとき入力　雇用者+業務内容を選択肢にする#IntegerFieldでは？
    comment=models.CharField(max_length=100, blank=True, null=True)#退勤のとき入力 
    approval=models.BooleanField(default=False)#employerが入力
    paid_flg=models.BooleanField(default=False)#defaultはFalse　支払い後Trueになる

    def __str__(self):
        return 'ID:' + self.employee_ID + '   ' + str(self.date) + str(self.time)  + ' has been recorded.' 


class Post_Report(models.Model):
    employee_ID=models.CharField(max_length=10, blank=True)
    clock_in_or_out=models.BooleanField()
    date=models.DateField()
    time=models.TimeField()
    job_description=models.CharField(max_length=100)
    comment=models.CharField(max_length=200, blank=True, null=True)
    approve_flg=models.BooleanField(default=False)#defaultはFalse employer承認後Trueになる


