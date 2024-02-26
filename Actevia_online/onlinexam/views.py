from django.shortcuts import render,redirect
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
import openpyxl
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import Courceform ,QuestionForm ,TeacherSalaryForm,UploadForm
from .models import Course ,Question ,Result
from django.db.models import Sum
from .resources import QuestionSource
from django.contrib import messages
from tablib import Dataset
from teacher.views import teacher_signIn
from django.contrib.auth.decorators import login_required, user_passes_test
from cridential.views import app_access_required


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return render(request ,"online/home.html")




def admin_login(request):
    error_message = None
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('/admin_dashboard')
            else:
                error_message = "You are not authorized to access this page."
        else:
            error_message = "Username or Password is incorrect!!!"
    
    return render(request , "online/admin_login.html",{'error_message': error_message})



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()



def after_login_view(request):
    if is_student(request.user):      
        return HttpResponseRedirect('/student/student_dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TeacherUser.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return HttpResponseRedirect('/teacher/teacher_dashboard')
        else:
            return render(request,'teacher/teacher_approval.html')
    else:
        return HttpResponseRedirect('/admin_dashboard')

# def after_login_view(request):
#     if is_student(request.user):      
#         return HttpResponseRedirect('/student/student_dashboard')
                
#     elif is_teacher(request.user):
#         teacher = TeacherUser.objects.filter(user_id=request.user.id , status = True)
#         if teacher:
#             if teacher.status:
#                 return HttpResponseRedirect('/teacher/teacher_dashboard')
#             else:
#                 return render(request, 'teacher/teacher_approval.html')
#         else:
#             return render(request, 'teacher/teacher_approval.html')
            
#     else:
#         return HttpResponseRedirect('/admin_dashboard')




def admin_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return HttpResponseRedirect('/admin_login')



@login_required(login_url=admin_login)
def after_login_page(request):
    return render(request , "online/after_login_page.html")


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_logout(request):
    logout(request)

    return redirect("lms_home")

from cridential.models import StudentUser,TeacherUser

@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_dashboard(request):
    dict={
    'total_student':StudentUser.objects.all().count(),
    'total_teacher':TeacherUser.objects.all().filter(status=True).count(),
    # 'total_teacher':TeacherUser.objects.all().count(),
    'total_course':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    }
    return render(request ,"online/admin_dashboard.html" ,{"dict":dict})




@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_teacher(request):
    dict={
    'total_teacher':TeacherUser.objects.all().filter(status=True).count(),
    'pending_teacher':TeacherUser.objects.all().filter(status=False).count(),
    'salary':TeacherUser.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request ,"online/admin_teacher.html" ,{"dict":dict})

@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_teacher_view(request):
    teachers= TeacherUser.objects.all().filter(status=True)
    return render(request,'online/admin_teacher_view.html',{'teachers':teachers})



from teacher.forms import TeacherForm , TeacherUserForm

@app_access_required('Learning Management')
@login_required(login_url='admin_login')
def admin_update_teacher(request, pk):
    teacher = TeacherUser.objects.get(id=pk)
    user = teacher.user
    userForm = TeacherUserForm(instance=user)
    teacherForm = TeacherForm(instance=teacher)
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}

    if request.method == 'POST':
        userForm = TeacherUserForm(request.POST, instance=user)
        teacherForm = TeacherForm(request.POST, instance=teacher)

        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(userForm.cleaned_data['password1'])
            user.save()

            teacherForm.save()
            return HttpResponseRedirect('/admin_teacher_view')

    return render(request, 'online/admin_update_teacher.html', {'my': mydict})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_delete_teacher(request ,pk):
    teacher=TeacherUser.objects.get(id=pk)
    user=teacher.user
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin_teacher_view')



@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_pending_teacher_view(request):
    teachers= TeacherUser.objects.all().filter(status=False)
    return render(request,'online/admin_pending_teacher_view.html',{'teachers':teachers})

@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_approved_teacher_view(request, pk):
    if request.method == 'POST':
        teacher = TeacherUser.objects.get(id=pk)
        teacher.status = True
        teacher.save()
        messages.success(request, f"Teacher {teacher.user} has been approved.")
        return HttpResponseRedirect('/admin_pending_teacher_view')

    teacher = TeacherUser.objects.get(id=pk)
    return render(request, 'online/admin_approved_teacher.html', {'teacher': teacher})

@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_reject_teacher_view(request ,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin_pending_teacher_view')


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'online/admin_teacher_salary_view.html',{'teachers':teachers})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_student(request):
    dict={
    'total_student':StudentUser.objects.all().count(),
    }
    return render(request ,"online/admin_student.html",{"dict":dict})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_view_student(request):
    students= StudentUser.objects.all()
    return render(request,'online/admin_view_student.html',{'students':students})

from student.forms import StudentForm ,StudentUserForm


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_update_student(request, pk):
    student = StudentUser.objects.get(id=pk)
    user = student.user
    userForm = StudentUserForm(instance=user)
    studentForm = StudentForm(instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}

    if request.method == 'POST':
        userForm = StudentUserForm(request.POST, instance=user)
        studentForm = StudentForm(request.POST, instance=student)

        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(userForm.cleaned_data['password1'])
            user.save()

            studentForm.save()
            return redirect('admin_view_student')

    return render(request, 'online/admin_update_student.html', {'my': mydict})



@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_delete_student(request ,pk):
    student = StudentUser.objects.get(id=pk)
    user = student.user
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin_view_student')









@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_cource(request):
    return render(request ,"online/admin_cource.html")


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_add_cource(request):
    Add_cource = Courceform()
    if request.method == "POST":
        Add_cource = Courceform(request.POST)
        if Add_cource.is_valid():
            Add_cource.save()

        else:
            print("<h1>Cource is not Save </h1>")

        return HttpResponseRedirect("/admin_view_cource")

    return render(request , 'online/admin_add_cource.html' ,{"Cource":Add_cource})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_view_cource(request):
    view_courses = Course.objects.all()
    return render(request,'online/admin_view_course.html',{'courses':view_courses})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_delete_cource(request ,pk):
    delete_cource = Course.objects.get(id=pk)
    delete_cource.delete()
    return HttpResponseRedirect("/admin_view_cource")





@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_question(request):
    return render(request ,"online/admin_questions.html")


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_add_questions(request):
    questionForm=QuestionForm()
    if request.method=='POST':
        questionForm=QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin_view_question')
    return render(request,'online/admin_add_question.html',{'questionForm':questionForm})


@app_access_required('Learning Management')
def admin_add_question_xl(request):
    form = UploadForm()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            workbook = openpyxl.load_workbook(uploaded_file)
            worksheet = workbook.active
            course_id = request.POST.get('course')
            course = Course.objects.get(id=course_id)
            for row in worksheet.iter_rows(min_row=2):
                question = Question(
                    course=course,
                    marks=row[0].value,
                      question=row[1].value,
                      option1=row[2].value,
                      option2=row[3].value,
                      option3=row[4].value,
                      option4=row[5].value,
                      answer=row[6].value
                      )
                question.save()
            return HttpResponseRedirect('/admin_view_question')
        else:
            form = UploadForm()
    # return render(request ,"online/xl.html" ,{'form': form, 'courses': Course.objects.all()})
    return render(request ,"online/xl.html" ,{"courses":Course.objects.all() ,"form":form})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_view_questions(request):
    view_questions = Course.objects.all()
    return render(request , "online/admin_view_question.html" ,{"question":view_questions})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_view_question_set(request ,pk):
    view_wuestion_set =Question.objects.all().filter(course_id=pk)
    return render(request ,"online/view_question_set.html",{"question":view_wuestion_set})


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_delete_question(request ,pk):
    question_delete = Question.objects.get(id=pk)
    question_delete.delete()
    return HttpResponseRedirect("/admin_view_question")


@app_access_required('Learning Management')
@login_required(login_url=teacher_signIn)
@login_required(login_url=admin_login)
def admin_view_student_marks(request):
    students= StudentUser.objects.all()
    return render(request,'online/admin_view_student_marks.html',{'students':students})

@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_view_marks(request ,pk):
    courses = Course.objects.all()
    response =  render(request,'online/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response


@app_access_required('Learning Management')
@login_required(login_url=admin_login)
def admin_check_marks(request ,pk):
    course = Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= StudentUser.objects.get(id=student_id)

    results=Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'online/admin_check_marks.html',{'results':results})


@app_access_required('Learning Management')
def admin_video(request):
    return render(request , "online/admin_video.html")



from cridential.views import app_access_required

@app_access_required('Learning Management')
@login_required(login_url='/login/')
@app_access_required('Project Management')
def collab(request):
    return render(request, "online/collab.html")








