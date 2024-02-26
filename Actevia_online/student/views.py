from django.shortcuts import get_object_or_404, render
from tablib import Dataset
# from .resources import MCResource
# from .models import MC
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import StudentForm, StudentUserForm
from django.contrib.auth.models import Group
from onlinexam import models as QMODEL
from teacher import models as TMODEL
from .models import Student
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import VideoPublication
from postapp.models import Post
import json
from teacher.models import CoursePublication
from onlinexam.models import Course
from django.db.models import F


def student_home(request):
    return render(request, "student/student_home.html")


def thank(request):
    return render(request, "student/thanks.html")


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import StudentUserForm, StudentForm
from django.contrib import messages

User = get_user_model()

from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login

# def student_signUp(request):
#     if request.method == 'POST':
#         user_form = StudentUserForm(request.POST)
#         student_form = StudentForm(request.POST)
#         if user_form.is_valid() and student_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password1'])
#             user.save()
#             student = student_form.save(commit=False)
#             student.user = user
#             student.save()

#             # Add the user to the STUDENT group
#             student_group, created = Group.objects.get_or_create(name='STUDENT')
#             user.groups.add(student_group)

#             # Authenticate and login the user
#             authenticated_user = authenticate(request, username=user_form.cleaned_data['username'],
#                                               password=user_form.cleaned_data['password1'])
#             if authenticated_user is not None:
#                 login(request, authenticated_user)
#                 return redirect('student_dashboard')  # Replace 'student_dashboard' with your student dashboard URL name
#             else:
#                 messages.error(request, 'Failed to authenticate user.')
#         else:
#             messages.error(request, 'Error occurred during registration. Please check the form.')
#     else:
#         user_form = StudentUserForm()
#         student_form = StudentForm()

#     return render(request, 'student/signup.html', {'user_form': user_form, 'student_form': student_form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def student_signUp(request):
    if request.method == 'POST':
        user_form = StudentUserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            # Add the user to the STUDENT group
            student_group, created = Group.objects.get_or_create(name='STUDENT')
            user.groups.add(student_group)

            return redirect('student_signin')  # Replace 'student_signin' with your student signin URL name
        else:
            # Print the form errors to console for debugging
            print(user_form.errors)
            print(student_form.errors)
            messages.error(request, 'Error occurred during registration. Please check the form.')
    else:
        user_form = StudentUserForm()
        student_form = StudentForm()

    return render(request, 'student/signup.html', {'user_form': user_form, 'student_form': student_form})




def Student_signIn(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            if user.groups.filter(name='STUDENT').exists():
                login(request, user)
                return HttpResponseRedirect('/student/student_dashboard')
            else:
                error_message = "You are not authorized to access this page."
        else:
            error_message = "Username or Password is incorrect!!!"

    return render(request, 'student/login.html',{'error_message': error_message})


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_logout(request):
    logout(request)

    return  redirect("lms_home")


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_dashboard(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }

    return render(request, "student/student_dashboard.html", {"dict": dict})


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_exam(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_tack_exam(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/student_take_exam.html', {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_start_exam(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/student_start_exam.html',
                      {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


from cridential.models import StudentUser
@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
# def calculate_marks_view(request):
#     if request.COOKIES.get('course_id') is not None:
#         course_id = request.COOKIES.get('course_id')
#         course=QMODEL.Course.objects.get(id=course_id)
#         total_marks=0
#         questions=QMODEL.Question.objects.all().filter(course=course)
#         for i in range(len(questions)):
#             selected_ans = request.COOKIES.get(str(i+1))
#             actual_answer = questions[i].answer
#             if selected_ans == actual_answer:
#                 total_marks = total_marks + questions[i].marks
#         student = Student.objects.get(user_id=request.user.id)
#         result = QMODEL.Result()
#         result.marks=total_marks
#         result.exam=course
#         result.student=student
#         result.save()
#         return HttpResponseRedirect('/student/thanks')



def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)
        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        result = None
        student = StudentUser.objects.get(user_id=request.user.id)
        try:
            result = QMODEL.Result.objects.get(exam=course, student=student)
        except QMODEL.Result.DoesNotExist:
            result = QMODEL.Result(exam=course, student=student, marks=0)
        result_count = QMODEL.Result.objects.filter(exam=course, student=student).count()
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        result.marks = total_marks
        result.attempts = result_count + 1
        result.save()
        # Create a JSON string from the marks value
        marks_json = json.dumps(str(total_marks))
        # Set the marks cookie with the JSON string
        response = HttpResponseRedirect('/student/thanks')
        for i in range(len(questions)):
            response.delete_cookie(str(i+1))
        response.delete_cookie('course_id')
        response.set_cookie('marks', marks_json)
        return response


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def studetn_view_result(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_view_result.html', {'courses': courses})


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_view_check_marks(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(
        onlinexam=course).filter(student=student)
    return render(request, 'student/student_check_marks.html', {'results': results})


@login_required(login_url='/student/student_signIn')
@user_passes_test(is_student)
def student_view_marks(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_view_marks.html', {'courses': courses})


from django import template
register = template.Library()

@register.simple_tag
def get_published_courses_url(student_id):
    student = StudentUser.objects.get(id=student_id)
    return view_published_courses(student)

def view_published_courses(request, pk):
    student = StudentUser.objects.get(id=pk)
    publications = CoursePublication.objects.filter(student=student)
    course_ids = [p.course.id for p in publications if not p.is_attended]
    courses = Course.objects.filter(id__in=course_ids).annotate(expiration_hours=F('coursepublication__expiration_hours'))
    
    return render(request, 'student/published_course.html', {'student': student, 'courses': courses})



def go_back1(request):
     return redirect('/student/student_dashboard')

def show_video(request ,pk):
    student= StudentUser.objects.get(pk=pk)
    publications = VideoPublication.objects.filter(student=student)
    video_ids = [p.video_file.id for p in publications]
    videos = Post.objects.filter(id__in=video_ids)
    context = {"videos":videos ,"student":student}
   
    return render(request ,'student/published_videos1.html' ,context)