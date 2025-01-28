from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('Log_In',views.Log_In,name='Log_In'),
    path('teacherSign',views.teacherSign,name='teacherSign'),
    path('studentSign',views.studentSign,name='studentSign'),
    path('adminHome',views.adminHome,name='adminHome'),
    path('teacherHome',views.teacherHome,name='teacherHome'),
    path('studentHome',views.studentHome,name='studentHome'),
    path('approval_request',views.approval_request,name='approval_request'),
    path('teacher_signup',views.teacher_signup,name='teacher_signup'),
    path('student_signup',views.student_signup,name='student_signup'),
    path('view_approvalrequests',views.view_approvalrequests,name='view_approvalrequests'),
    path('Fun_login',views.Fun_login,name='Fun_login'),
    path('approveRequest/<int:ud>',views.approveRequest,name='approveRequest'),
    path('disapproveRequest/<int:ud>',views.disapproveRequest,name='disapproveRequest'),
    path('LogOut',views.LogOut,name='LogOut'),
    path('reset_pswd',views.reset_pswd,name='reset_pswd'),
    path('reset_password',views.reset_password,name='reset_password'),
    path('streset_password',views.streset_password,name='streset_password')
]