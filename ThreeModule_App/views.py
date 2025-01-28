from django.shortcuts import render,redirect
from ThreeModule_App.models import CustomUser,Teachers,Students
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import auth
from django.db.models import Q
import random
import os
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'home.html')

def teacherSign(request):
    return render(request,'teacher_signup.html')

def studentSign(request):
    return render(request,'student_signup.html')

def teacherHome(request):
    return render(request,'teacherhome.html')

def studentHome(request):
    return render(request,'studenthome.html')


def approval_request(request):
    return render(request,'approval_request.html')

def teacher_signup(request):
        if request.method == 'POST':
            first_name=request.POST['fname']
            last_name=request.POST['lname']
            username=request.POST['username']
            email=request.POST['email']
            user_type=request.POST['type']
            age=request.POST['age']
            phone_number=request.POST['phn']
            image=request.FILES['img']
            courses=request.POST['courses']
            if CustomUser.objects.filter(username = username).exists():
                messages.info(request,'This Username already Exists..!!')
                return redirect('teacherSign')
        
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'This email already Exists..!!')
                return redirect('teacherSign')

            else:
                teacher=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,user_type=user_type)
                teacher1=Teachers(Age=age,Phone_number=phone_number,Image=image,Course=courses,User=teacher)
                teacher1.save()
                # messages.success(request,'Registration Successfull. Please wait for admin approval')
                return redirect('home')


def student_signup(request):
        if request.method == 'POST':
            first_name=request.POST['fname']
            last_name=request.POST['lname']
            username=request.POST['username']
            email=request.POST['email']
            user_type=request.POST['type']
            age=request.POST['age']
            phone_number=request.POST['phn']
            image=request.FILES['img']
            courses=request.POST['courses']
            if CustomUser.objects.filter(username = username).exists():
                messages.info(request,'This Username already Exists..!!')
                return redirect('studentSign')
        
            if CustomUser.objects.filter(email = email).exists():
                messages.info(request,'This email already Exists..!!')
                return redirect('studentSign')

            else:
                student=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,user_type=user_type)
                student1=Students(Age=age,Phone_number=phone_number,Image=image,Course=courses,User=student)
                student1.save()
                # messages.success(request,'Registration Successfull. Please wait for admin approval')
                return redirect('home')
            

def Log_In(request):
    return render(request,'login.html')


def Fun_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['pswd']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('adminHome')
            elif user.user_type == '2':
                login(request,user)
                return redirect('teacherHome')
            elif user.user_type == '3':
                login(request,user)
                return redirect('studentHome')
        else:
            messages.info(request,'Invalid Username or Password')
            return redirect('Log_In') 


def adminHome(request):
    req_counts=CustomUser.objects.filter(status=0).count()
    req_count=req_counts-1
    # print(req_count)
    return render(request,'adminhome.html',{'request_counts':req_count})


def view_approvalrequests(request):
    users=CustomUser.objects.filter(~Q(user_type = '1'))
    req_counts=CustomUser.objects.filter(status=0).count()
    req_count=req_counts-1
    # print(req_count)
    return render(request,'viewapproval_request.html',{'user_data':users,'request_counts':req_count})


def approveRequest(request, ud):
    user = CustomUser.objects.get(id=ud)
    user.status = 1
    user.save()

    if user.user_type == '2':
        teacher = Teachers.objects.get(User=user)
        password = str(random.randint(100000, 999999))
        print(password)
        user.set_password(password)
        user.save()

        send_mail(
            'Admin approved', 
            f'Username: {teacher.User.username}\nPassword: {password}\nEmail: {teacher.User.email}',
            settings.EMAIL_HOST_USER,
            [teacher.User.email],
        )
        # messages.info(request, 'Approved Teacher')

    elif user.user_type == '3': 
        password = str(random.randint(100000, 999999))
        user.set_password(password)
        user.save()

        send_mail(
            'Admin approved',
            f'Username: {user.username}\nPassword: {password}\nEmail: {user.email}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        # messages.info(request, 'Approved Student')

    return redirect('view_approvalrequests')


def disapproveRequest(request, ud):
    user1 = CustomUser.objects.get(id=ud)
    if user1.user_type == '2':
        user4 = Teachers.objects.filter(User=ud).first()
        if user4 and user4.Image and os.path.isfile(user4.Image.path):
            os.remove(user4.Image.path)
        Teachers.objects.filter(User=ud).delete()

    elif user1.user_type == '3':
        user5 = Students.objects.filter(User=ud).first()
        if user5 and hasattr(user5, 'Image') and user5.Image and os.path.isfile(user5.Image.path):
            os.remove(user5.Image.path) 
        Students.objects.filter(User=ud).delete()

    user1.delete()

    send_mail(
        'Admin disapproved',
        'Dear User, your request has been disapproved by the admin.',
        settings.EMAIL_HOST_USER,
        [user1.email],
    )

    return redirect('view_approvalrequests')
    

def LogOut(request):
    auth.logout(request)  
    return redirect('home')


def reset_pswd(request):
    return render(request,'reset_password.html')


def streset_password(request):
    return render(request,'streset_password.html')


def reset_password(request):
    if request.method == 'POST':
        new_pswd = request.POST['npswd']
        confirm_pswd = request.POST['cfpswd']
        if new_pswd == confirm_pswd:
            if len(new_pswd) < 6 or not any(char.isupper() for char in new_pswd) \
                or not any(char.isdigit() for char in new_pswd) \
                or not any(char in '!@#$%^&*()_+-=[]{};:,.<>?/~' for char in new_pswd):
                messages.error(request, 'Password must be at least 6 characters long and contain at least one upper case, one digit and one special character.')
                return redirect('reset_password') 
            else:  
                usr = request.user.id
                tsr = CustomUser.objects.get(id=usr)
                tsr.set_password(new_pswd)
                tsr.save()
                messages.info(request, "Password Changed")
                return redirect('reset_password')
        else:
            messages.error(request, "Passwords do not match.") 
            return redirect('reset_password')
    return render(request, 'reset_password.html')
