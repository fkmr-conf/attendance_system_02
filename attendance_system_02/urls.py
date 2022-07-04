from django.urls import path
from . import views
#from .views import contractList
#from .views import contractDetail

urlpatterns=[
    #テスト
    path('test', views.Employer_function().test, name='test'),

    #ログイン
    path('employer_log_in', views.Employer_function().log_in, name='employer_log_in'),
    path('employee_log_in', views.Employee_function().log_in, name='employee_log_in'),

    #メニュー
    path('employer_menue', views.Employer_function().menue, name='employer_menue'),
    path('employee_menue', views.Employee_function().menue, name='employee_menue'),   

    #ログアウト
    #path('employer_log_out', views.Employer_function().log_out, name='employer_log_out'),
    #path('employer_log_out', views.Employee_function().log_out, name='employee_log_out'),

    #パスワード変更
    path('employer_change_password', views.Employer_function().change_password, name='employer_change_pw'),
    path('employee_change_password', views.Employee_function().change_password, name='employee_change_pw'),

    #被雇用者・契約の登録
    path('employment_registration_ID', views.Employer_function()._ID_check, name='rgs_ID'),
    path('employment_registration_emp', views.Employer_function()._emp_register, name='rgs_employee'),
    path('employment_registration_cnt', views.Employer_function()._cnt_register, name='rgs_contract'),

    #契約の確認
    path('see_contracts', views.Employer_function()._see_contracts, name='see_contracts'),

    #
    path('approval_unit', views.Employer_function()._choose_approval_type, name='approval_unit'),

    #勤務申請の承認
    path('select_post_report', views.Employer_function()._select_post_report, name='select_post_report'),
    path('approve_report/<int:num>', views.Employer_function()._approve_report, name="approve_post_report"),

    #打刻
    path('record_clock', views.Employee_function()._clock, name='rec_clock'),
    path('record_clock', views.Employee_function()._clock, name='clock'),    
    path('rec_clk_jd_selection', views.Employee_function()._select_jd, name='select_jd'),
    path('rec_clk_comment', views.Employee_function()._comment, name='comment'),

    #契約の確認
    path('check_contract', views.Employee_function()._check_my_cnt, name='check_my_cnt'),

    #勤務申請
    path('post_working_report', views.Employee_function()._post_report, name='post_working_report'),
    
    #
    path('check_my_working_report', views.Employee_function()._check_my_working_report, name='check_my_working_report'),

    #給与計算
    path('choose_approval_type', views.Employer_function()._choose_approval_type, name='choose_approval_type'),
    #
    path('daily_approve', views.Employer_function()._daily_approve, name='daily_approve'),
    #
    path('indivisual_approve', views.Employer_function()._indivisual_approve, name='indivisual_approve'),

]