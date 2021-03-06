from typing import ParamSpecKwargs
from urllib.request import Request
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q, Min, Max
from django.views.generic.edit import FormView
#from django.views.generic.edit import  ModelFormMixin


from .models import Employer
from .models import Employee
from .models import Contract
from .models import working_record
from .models import Post_Report
#from .models import TEST_Post_Report############################################

from .forms import comment_form, log_in_form
from .forms import ID_form
from .forms import employee_registration
from .forms import contract_registration
from .forms import change_password
from .forms import see_contracts_form
from .forms import jd_selection_form
from .forms import comment_form
from .forms import post_report_form
from .forms import select_year_month_form

import datetime
from dateutil.relativedelta import relativedelta

#from .forms import see_contracts_form

# Create your views here.


Employer_menue_dic={
        'Register Employee': '<a href=employment_registration_ID',
        'See Contracts':'<a href=see_contracts',
        'Check Working Report':'<a href=check_workrep',
        'Approve POST-Working Report':'<a href=select_post_report',
        'Calculate Salary':'<a href=approval_unit',
        'Change Password': '<a href=employer_change_password'
        }

Employee_menue_dic={
        'Clock_in/out':'<a href=record_clock',
        'See Contracts':'<a href=see_contracts', 
        'Check Working Report':'<a href=check_my_working_report', 
        'Post Working Report':'<a href=post_working_report', 
        'Change Password': '<a href=employee_change_password'
        }


class Employer_function():
    def __init__(self):
        self.model=Employer
        self.note=''
        self.position='employer'
        self.menue_dic=Employer_menue_dic
    
    def log_in(self, request):
        next_step_flg=False
        params={
            'title':'Attendance Systen for '+ self.position +'-side',
            'message':'Please enter your ID and Password',
            'form':log_in_form(),
            'note':self.note,
            'position':self.position,
        }
        if (request.method=='POST'):
            search_ID=request.POST['ID']
            if len(self.model.objects.filter(IDcode=search_ID))>0:#(1)???????????????ID???DB???????????????
                user=self.model.objects.get(IDcode=search_ID)

                if request.POST['password']==user.log_in_password:#(2)???????????????????????????????????????ID????????????????????????
                    params['note']=''
                    #????????????????????????
                    request.session['ID']=search_ID
                    request.session['password']=user.log_in_password
                    #???????????????????????????
                    next_step_flg=True
                
                else:#(2)???????????????????????????????????????
                    params['message']='ERROR: The password is incorrect.'

            else:#(1)DB??????????????????ID?????????
                params['message']='ERROR: Invalid ID.'
            
        if next_step_flg:
            return redirect('/attendance_system_02/'+ self.position + '_menue')
        else:
            return render(request, 'log_in.html', params)

    def menue(self, request):
        visitor=self.model.objects.get(IDcode=request.session['ID']).name
        params={
            'position':self.position,
            'title':'MENUE for ' + self.position,
            'message':'WELCOME, ' + visitor,
            'choice': self.menue_dic
        }

        if request.method=='POST':
            request.session.clear()
            return redirect('/attendance_system_02/'+ self.position + '_log_in')

        return render(request, 'menue.html', params)


    def _ID_check(self,request):
        params={
            'title':'',
            'message':'Please fill in the ID of the employee to be employed.',
            'form':ID_form
        }
        if (request.method=='POST'):
            request.session['empID']=request.POST['Input_ID']
            if len(Employee.objects.filter(IDcode=request.session['empID']))>0:#ID???Employee??????????????????????????????
                return redirect('rgs_contract')
            else:#ID???Employee????????????????????????
                return redirect('rgs_employee')       
        return render(request, 'rgs_ID.html', params)
    

    def _emp_register(self, request):
        params={
            'title':'Employee Registration',
            'message':'Please fill in the employee\'s information.',
            'form':employee_registration
        }
        
        
        if (request.method=='POST'):
            the_employee=Employee(
                IDcode=request.session['empID'],
                name=request.POST['name'],
                tax_category=request.POST['tax_category']
            )
            the_employee.save()
            return redirect('rgs_contract')
        
        return render(request, 'rgs_emp.html', params)
    
    
    def _cnt_register(self, request):
        
        if Employee.objects.get(IDcode=request.session['empID']).tax_category==1:
            tax_cate='???'
        else:
            tax_cate='???'

        params={
            'registered_ID':request.session['empID'],
            'registered_name':Employee.objects.get(IDcode=request.session['empID']).name,
            'registered_tax_cate':tax_cate,
            'form':contract_registration
        }
        
        #????????????post????????????
        if (request.method=='POST'):
            the_contract=Contract(
                cnt_employee=request.session['empID'],
                cnt_employer=request.session['ID'],
                contract_start=request.POST['contract_start'],
                contract_end=request.POST['contract_end'],
                wage_per_hour=request.POST['wage_per_hour'],
                job_description=request.POST['job_description'],
                day_off=request.POST['day_off'],           
            )
            the_contract.save()
            del request.session['empID']
            return redirect('/attendance_system_02/'+ self.position + '_menue')         
        
        return render(request, 'rgs_cnt.html', params)


    def change_password(self, request):
        params={
            'position':self.position,
            'title':'Change Password',
            'message':'Please fill in your current password and new password.',
            'form': change_password
        }    
        if (request.method=='POST'):
            #(1)???????????????currentpw???????????????????????????????????????????????????
            if request.POST['current_pass']==request.session['password']:#(1)YES
                #(2)2??????????????????NEWpw??????????????????
                if request.POST['NEW_pw_01']==request.POST['NEW_pw_02']:#(2)YES
                    target=self.model.objects.get(IDcode=request.session['ID'])
                    target.log_in_password=request.POST['NEW_pw_01']
                    target.save()
                    #????????????????????????????????????pw?????????
                    request.session['password']=request.POST['NEW_pw_01']
                    params['message']='Your password has been changed successfully.'
                
                else:#(2)NO
                    params['message']='The first one and second one you typed in as a NEW password is NOT same.'

            else:#(1)NO
                params['message']='The current password is NOT correct.'
            
        return render(request, 'change_pw.html', params)

############################################################################################################################
    def add_employee_name(self, filtered_queryset):
        list_to_add=list(filtered_queryset.values())
        for cnt_dic in list_to_add:
            theID=cnt_dic['cnt_employee']
            cnt_dic['name']=Employee.objects.get(IDcode=theID).name
        return list_to_add

    def test(self, request):
        mylist=self.add_employee_name(Contract.objects.filter(cnt_employer='Employer01'))
        return HttpResponse(len(mylist))
 
    
    def _see_contracts(self, request):
        emp_by_you= Contract.objects.filter(cnt_employer=request.session['ID'])
        #Contract model?????????????????????????????????????????????????????????
        all_contract_emp_by_you=self.add_employee_name(emp_by_you)
        
        params={
            'whole_title':'See Contracts',
            'form': see_contracts_form,
            'search_flg': False,
            'title_1':'All Contracts',
            'table_1': all_contract_emp_by_you,            
        }

        if (request.method=='POST'):#?????????????????????????????????
            basis=request.POST['basis_date']
            valid_contracts=self.add_employee_name(emp_by_you.filter(contract_start__lte=basis, contract_end__gte=basis))
            expired_contracts=self.add_employee_name(emp_by_you.filter(Q(contract_start__gt=basis) |Q(contract_end__lt=basis)))

            params['search_flg']=True
            params['title_1']='Valid Contracts'#?????????????????????????????????
            params['table_1']=valid_contracts
            params['title_2']='Planeed or Expired Contracts'#???????????????????????????????????????or??????
            params['table_2']=expired_contracts
            params['basis']=basis


        return render(request, 'see_contracts.html', params)

    

    def _make_my_cnt_list(self, request):
        #?????????cnt_employer?????????Contract???ID?????????????????????
        my_cnt_list=[]
        #7
        for each_cnt in Contract.objects.filter(cnt_employer=request.session['ID']):
            my_cnt_list.append(each_cnt.id)
        return my_cnt_list

    def _make_list_of_dic(self, request):#???????????????????????????????????????
        #Post_Report???????????????????????????flag???False?????????job_description???=????????????Contact???ID??????my_cnt_list???=????????????????????????????????????
        #?????????ID????????????????????????????????????????????????????????????
        my_cnt_list=self._make_my_cnt_list(request)
        filtered_post_report=Post_Report.objects.filter(approve_flg=False, job_description__in=my_cnt_list)
        list_of_dic=[]
        for a_report in filtered_post_report:
            temp_dic={}
            temp_dic['id']=a_report.id
            temp_dic['EMPLOYEE_ID']=a_report.employee_ID
            #Post???Report??????IDcode??????????????????????????????????????????????????????????????????Employee?????????????????????
            temp_dic['NAME']=Employee.objects.get(IDcode=a_report.employee_ID).name
            temp_dic['DATE']=a_report.date
            temp_dic['TIME']=a_report.time
            
            if a_report.clock_in_or_out:
                temp_dic['IN_OR_OUT']='IN'
            else:
                temp_dic['IN_OR_OUT']='OUT'
            #Post???Report???job_description??????Contract???id???????????????????????????????????????????????????????????????Contract????????????job_description?????????           
            temp_dic['JOB_DESCRIPTION']=Contract.objects.get(id=a_report.job_description).job_description

            temp_dic['comment']=a_report.comment
            list_of_dic.append(temp_dic)

        return list_of_dic

    def make_currender(self, the_date):
        #????????????key?????????dictionary??????????????????????????????(????????????employee_ID,contract_ID,IN,OUT,Comment????????????key???????????????????????????)
        #?????????????????????????????????1??????????????????????????????
        target_year=the_date.year
        target_month=the_date.month
        first_date=datetime.datetime(target_year,target_month,1)
        misoka_date=first_date + datetime.timedelta(days=-1) + relativedelta(months=1)#?????? timedelta???month?????????
        #6
        currender_list=[]
        date_to_add=first_date
        while True:
            temp_dic={'DATE':date_to_add}
            currender_list.append(temp_dic)
            if date_to_add==misoka_date:
                break
            date_to_add=date_to_add + datetime.timedelta(days=1)

        return currender_list



    def _select_post_report(self, request):
        list_of_dic=self._make_list_of_dic(request)
    
        params={
            'title':'Approve Post Working Report',
            'table':list_of_dic,
        }
        #???????????????Post_Report???job_description???contract???id??????????????????
        #id??????????????????contract????????????????????????cnt_employer????????????request.session[ID???????????????table???????????????
        #????????????????????????????????????????????????Post_Report???approve_flg=True????????????????????????working_record????????????????????????
        
        return render(request, 'select_post_report.html', params)

    
    def make_monthly_report(self, request, the_date, employee_ID):
        currender_list=self.make_currender(the_date)
        for one_day in currender_list:
            #one_day={'DATE':datetime.datetime(2022,x,x,0,0)}???
            #one_day={'DATE':datetime.datetime(2022,x,x,0,0),'RECORD':[{'IN':8:00, 'OUT':15:00},{},{}]}
            #
            #time???????????????????????????        
            records=working_record.objects.filter(
                employee_ID=employee_ID,
                date=one_day['DATE'],
            ).order_by('time')
            
            one_day['RECORD']=[]

            if len(records)>0:
                for record in records:
                    if record.clock_in_or_out:#????????????
                        temp_dic={'IN':record.time, 'OUT':''}
                        one_day['RECORD'].append(temp_dic)
                        del temp_dic
                    else:#????????????
                        if one_day['RECORD']==[] or one_day['RECORD'][-1]['OUT']!='':
                            temp_dic={'IN':'', 'OUT':record.time}
                            one_day['RECORD'].append(temp_dic)
                            del temp_dic
                        else:
                            one_day['RECORD'][-1]['OUT']=record.time
        
        return currender_list#?


    def _approve_report(self, request, num):
        the_report=Post_Report.objects.get(id=num)
        #????????????
        if the_report.clock_in_or_out:
            clock_in_or_out='IN'
        else:
            clock_in_or_out='OUT'
        report_dic={
            'employee_ID':the_report.employee_ID,
            'employee_name':Employee.objects.get(IDcode=the_report.employee_ID).name,
            'date':the_report.date.strftime('%Y/%m/%d'),
            'time':the_report.time,
            'in_or_out':clock_in_or_out,
            'job_description':Contract.objects.get(id=the_report.job_description).job_description,
            'comment':the_report.comment
        }
        
        currender_list=self.make_monthly_report(request, the_report.date, the_report.employee_ID)                             

        params={
            'title':'Approve Post Report',
            'YEAR_MONTH':'',
            'REPORT':report_dic,
            'CURRENDER':currender_list,

        }
         
        if request.method=='POST':
            #??????????????????true???
            the_report.application_flg=True
            #post??????????????????
            post_to_be_registered=working_record(
                employee_ID=the_report.employee_ID,
                date=the_report.date,
                time=the_report.time,
                clock_in_or_out=the_report.clock_in_or_out,
                job_description=the_report.job_description,
                comment=the_report.comment                
            )
            post_to_be_registered.save()
            #return redirect()

        return render(request, 'approve_post_report.html', params)


    #????????????
    #?????????????????????????????????paid_flg???False???working_record????????????????????????
    # ?????????????????????????????????yes??????paid_flg=True
    #  ??? ????????????employee??????working_record???True??????????????????employer???employee????????????????????????????????????????????????
    #
    def _calc_salary(self, request):
        form_1=""#??????????????????????????????????????????????????????
        form_2 = select_year_month_form()#paid_flg???False????????????????????????????????????
        
        unpaid_year_month_choice=[]
        form_2.fields['year_and_month'].choices=unpaid_year_month_choice


        params={
            'form_1':form_1,
            'form_2':form_2,
        }
        return render(request, '', params)

    """
    #???????????????????????????????????????
    def _choose_approval_type(self, request):#??????
        params={}
        if request.method=='POST':
            if 'daily' in request.POST:
                return redirect()
            elif 'indivisual' in request.POST:
                return redirect()
        return render(request, 'approval_unit_choice.html', params)

    def _daily_approve(self, request):
        return render()

    def _indivisual_approve(self, request):
        return render()
    """
    """
    def log_out(self, request):
        request.session.clear()
        return redirect('/attendance_system_02/'+ self.position + 'log_in')
    """

class Employee_function(Employer_function):
    def __init__(self):
        self.model=Employee
        self.note='IF you log in this system for the first time, please enter \"000\" as password '
        self.position='employee'
        self.menue_dic=Employee_menue_dic
    
    def _check_my_cnt(self, request):#????????????Employer_function()._see_contracts??????????????????
        my_cnt=Contract.objects.filter(cnt_employee=request.session['ID'])
        params={
            'whole_title':'Check My Contracts',
            'form':see_contracts_form,
            'search_flg':False,
            'title_1':'All Contracts',
            'table_1':my_cnt
        }
        if request.method=='POST':
            basis=request.POST['basis_date']
            params['search_flg']=True
            params['title_1']='Valid Contracts'
            params['table_1']=my_cnt.filter(contract_start__lte=basis, contract_end__gte=basis)
            params['title_2']='Expired Contracts'
            params['table_2']=my_cnt.filter( \
                Q(contract_start__gt=basis) |Q(contract_end__lt=basis) \
                )
            params['basis']=basis
        return render(request, 'see_contract.html', params)
        


    def _clock(self, request):
        dt=datetime.datetime.now()

        if request.method=='POST':
            if 'in' in request.POST:#??????
                in_out=True
            elif 'out' in request.POST:#??????
                in_out=False
            time_rec=working_record(
                employee_ID=request.session['ID'],
                date=datetime.date.today(),
                time=dt.time(),
                clock_in_or_out=in_out
            )
            time_rec.save()
            #???????????????????????????working_record???ID???????????????????????????
            request.session['time_record_ID']=time_rec.id
        
            if in_out:#??????
                #job_description?????????
                return redirect('/attendance_system_02/rec_clk_jd_selection')

            else:
                #comment?????????
                return redirect('/attendance_system_02/rec_clk_comment')
                #5
        return render(request, 'clock.html', {'title':'Clock In/Out'})
    
    
    def _create_jd_choice(self, request):
        #4
        jd_choice=[]#(contract???ID???model??????????????????, ????????????+????????????=HTML??????????????????)
        #list???tuple????????????????????????????????????tuple(jd_choice)
        for mycnt in Contract.objects.filter(cnt_employee=request.session['ID']):
            contract_ID=mycnt.id
            emp_name=Employer.objects.get(IDcode=mycnt.cnt_employer).name
            employer_name_and_jd=emp_name + "???" + mycnt.job_description
            jd_choice.append((contract_ID,employer_name_and_jd))
        return jd_choice
        
    def _select_jd(self, request):

        jd_choice=self._create_jd_choice(request)
        form= jd_selection_form()
        form.fields['job_description'].choices=jd_choice

        params={
            'form':form,
            'TEST':jd_choice,#TEST
        }

        if request.method=='POST':
            #?????????????????????????????????????????????     
            target=working_record.objects.get(id=request.session['time_record_ID'])
            target.job_description=request.POST['job_description']
            target.save()
            return redirect('http://localhost:8000/attendance_system_02/employee_menue')


        return render(request, 'clock_jd_select.html', params)

    def _comment(self, request):
        params={
            'form':comment_form,
        }
        if request.method=='POST':
            #?????????????????????????????????????????????
            target=working_record.objects.get(id=request.session['time_record_ID'])
            target.comment=request.POST['comment']
            target.save()
            del request.session['time_record_ID']
            return redirect('http://localhost:8000/attendance_system_02/employee_menue')
        
        return render(request,'clock_comment.html', params)


    def _post_report(self, request):
        jd_choice=self._create_jd_choice(request)
        form= post_report_form()
        form.fields['job_description'].choices=jd_choice
 
        params={
            'form':form,
        }

        if request.method=='POST':
            the_post=Post_Report(
                employee_ID=request.session['ID'],
                clock_in_or_out=request.POST['clock_in_or_out'],
                date=request.POST['date'],
                time=request.POST['time'],
                job_description=request.POST['job_description'],
                comment=request.POST['comment']
            )
            the_post.save()
           
            return redirect('http://localhost:8000/attendance_system_02/employee_menue')

        return render(request, 'post_report.html', params)

#?????????????????????????????????Employer_function()._approve_report????????????????????????????????????
    
    def _create_year_month_choice(self, request, idcode, num):
        #date??????????????????????????????working report?????????
        """
        num=0
        num=1
        """
        target=working_record.objects.filter(employee_ID=idcode)
        if num==0:
            pass
        elif num==1:
            target=target.filter(paid_flg=False)
        #3            
        first=target.aggregate(Min('date'))['date__min']
        latest=target.aggregate(Max('date'))['date__max']

        year_month_list=[]
        the_date=first
        while True:
            year_month=str(the_date.year) + " / " + str(the_date.month)#########first???None??????????????????##################################################
            if len(year_month_list) > 0 and year_month_list[-1][1]==year_month:
                pass
            else:
                year_month_list.append((the_date, year_month))

            if the_date==latest:
                break

            the_date += datetime.timedelta(days=1)

        return year_month_list
    
 
    def _check_my_working_report(self, request):
        
        year_month_choice=self._create_year_month_choice(request, request.session['ID'], 0)
        #??????????????????
        form=select_year_month_form()
        form.fields['year_and_month'].choices=year_month_choice

        if request.method=='POST':
            the_basis_date_str=request.POST['year_and_month']#??????????????????????????????
            #str?????????????????????????????????
            the_basis_date=datetime.datetime.strptime(the_basis_date_str, '%Y-%m-%d')
        else:
            the_basis_date=datetime.date.today()#
        working_currender_list=self.make_monthly_report(request, the_basis_date, request.session['ID'])


        params={
            "form":form,
            "CURRENDER":working_currender_list,

        }

        #???????????????????????????????????????????????????
        

        return render(request, 'see_my_working_report.html', params)


"""
#http://localhost:8000/attendance_system_02/rec_clk_jd_selection
    
#https://itc.tokyo/django/formview/  

"""





#https://blog.pyq.jp/entry/Python_kaiketsu_200421
#https://itc.tokyo/django/change-dynamically-values-of-choices/

#####################################################################
 