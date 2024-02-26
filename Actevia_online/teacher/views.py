from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
import openpyxl
# Create your views here.

from teacher.models import Teacher,CoursePublication
from onlinexam.models import Course, Question
from django.contrib.auth import authenticate, login, logout
from .forms import TeacherForm, TeacherUserForm, UploadForm
from django.contrib.auth.models import Group
from onlinexam import models as QMODEL
from student import models as SMODEL
from onlinexam import forms as QFORM
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from postapp.models import Post
from student.models import Student, VideoPublication 


def Teacher_home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/after_login')
    return render(request, "teacher/teacher_home.html")

from django.contrib import messages



def teacher_signUp(request):
    if request.method == 'POST':
        user_form = TeacherUserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            # Add the user to the TEACHER group
            teacher_group, created = Group.objects.get_or_create(name='TEACHER')
            user.groups.add(teacher_group)

            return redirect('teacher_signIn')  # Replace 'teacher_signIn' with your teacher sign-in URL name
        else:
            # Print the form errors to the console for debugging
            print(user_form.errors)
            print(teacher_form.errors)
            messages.error(request, 'Error occurred during registration. Please check the form.')
    else:
        user_form = TeacherUserForm()
        teacher_form = TeacherForm()

    return render(request, 'teacher/teacher_signup.html', {'user_form': user_form, 'teacher_form': teacher_form})



def teacher_signIn(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            if user.groups.filter(name='TEACHER').exists():
                login(request, user)
                return redirect("admin_click_view")
            else:
                error_message = "You are not authorized to access this page."
        else:
            error_message = "Username or Password is incorrect!!!"
    return render(request, 'teacher/teacher_signin.html',{'error_message': error_message})


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


# @login_required(login_url='teacher_signIp')
# @user_passes_test(is_teacher)
def Teacher_logout(request):
    logout(request)

    return redirect("lms_home")

from cridential.models import StudentUser
@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_student': StudentUser.objects.all().count()
    }
    return render(request, "teacher/teacher_dashboard.html", {"dict": dict})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_exam(request):
    return render(request, 'teacher/teacher_exam.html')


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_add_exam_cource(request):
    courseForm = QFORM.Courceform()
    if request.method == 'POST':
        courseForm = QFORM.Courceform(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher_view_exam_cource')
    return render(request, 'teacher/teacher_add_exam_cource.html', {'courseForm': courseForm})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_view_exam_cource(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam_cource.html', {'courses': courses})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_delete_exam_cource(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher_view_exam_cource')


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_question(request):
    return render(request, 'teacher/teacher_question.html')


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_add_question(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher_view_question')
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_view_question(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_see_question(request, pk):
    questions = QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request, 'teacher/teacher_see_question.html', {'questions': questions})


@login_required(login_url='/teacher/teacher_signIn')
@user_passes_test(is_teacher)
def teacher_delete_question(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher_view_question')

@login_required(login_url='/teacher/teacher_signIn')
def teacher_xl_add_question(request):
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
            return HttpResponseRedirect('/teacher/teacher_view_question')
        else:
            form = UploadForm()

    return render(request, "teacher/xl.html", {"courses": Course.objects.all(), "form": form})

@login_required(login_url='/teacher/teacher_signIn')
def teacher_view_student_marks(request):
    students = StudentUser.objects.all()
    return render(request, 'teacher/teacher_view_student_marks.html', {'students': students})

@login_required(login_url='/teacher/teacher_signIn')
def teacher_view_marks(request, pk):
    courses = Course.objects.all()
    response = render(
        request, 'teacher/teacher_view_marks.html', {'courses': courses})
    response.set_cookie('student_id', str(pk))
    return response


@login_required(login_url='/teacher/teacher_signIn')
def teacher_check_marks(request, pk):
    course = Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = StudentUser.objects.get(id=student_id)

    results = QMODEL.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'teacher/teacher_check_marks.html', {'results': results})


def teacher_video(request):

    return render(request, "teacher/teacher_video.html")



def teacher_publish(request):
   
       
    return render(request, 'teacher/publish_video.html')

@login_required
def publish_post(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        video_ids = request.POST.getlist('videos')
        print(video_ids)
        all_videos = request.POST.get('all_videos') == 'all'

        if all_videos:
            # Get a list of all videos uploaded by the currently logged in teacher
            videos = Post.objects.filter(teacher=request.user.teacher_profile)
        else:
            # Get the selected video objects uploaded by the currently logged in teacher
            videos = Post.objects.filter(id__in=video_ids, teacher=request.user.teacher_profile)

        if student_id == 'all':
            # Get a list of all students and publish the videos to each one of them
            students = StudentUser.objects.all()
            for student in students:
                # Publish the selected videos to the student
                for video in videos:
                    publication = VideoPublication.objects.create(student=student, video_file=video)

            response_message = f'Published {len(videos)} videos to all students. <a href="{reverse("go_back")}" class="back_btn" style="border-radius:0px;">Back</a>'

        else:
            # Get the selected student object and publish the selected videos to that student
            student = StudentUser.objects.get(id=student_id)
            # Publish the selected videos to the student
            for video in videos:
                publication = VideoPublication.objects.create(student=student, video_file=video)
            response_message = f'Published {len(videos)} videos to {student.user} {student.user.email}. '
            back_url = reverse('go_back')
            response_message += f'<a href="{back_url}" class="back_btn" style="border-radius:0px;">Back</a>'

        return HttpResponse(response_message)

    else:
        # Get a list of all students
        students = StudentUser.objects.all()
        # Render the form with the list of available videos uploaded by the currently logged in teacher and students
        videos = Post.objects.filter(teacher=request.user.teacher_profile)
        return render(request, 'teacher/publish_video.html', {'videos': videos, 'students': students})


def view_published_videos(request, pk):
    try:
        student = StudentUser.objects.get(id=pk)
    except Student.DoesNotExist:
        return HttpResponse('Student not found', status=404)
    
    publications = VideoPublication.objects.filter(student=student)
    video_ids = [p.video_file.id for p in publications]
    videos = Post.objects.filter(video_file__id=video_ids, video_publications__student=student)
    
    return render(request, 'teacher/views_published_videos.html', {'student': student, 'videos': videos})



def publish_course(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        expiration_days = request.POST.get('expiration_days')
        expiration_hours = request.POST.get('expiration_hours')

        print(student_id)
        print(course_id)

      
        student = StudentUser.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        print(student.user)
        print(course.course_name)
        
        # Publish the course to the student
        publication = CoursePublication.objects.create(student=student, course=course, expiration_days=expiration_days, expiration_hours=expiration_hours)
        publication.set_expiration_time()
        
        # Generate the URL for the go_back view
        back_url = reverse('go_back1')
        response_message = f'Published {course.course_name} course to {student.user.username}  {student.user.email}. <a href="{back_url}" class="back_btn" style="border-radius:0px;">Back</a>'
        return HttpResponse(response_message)
    
    
    
    else:
        # Get a list of all students and courses
        students = StudentUser.objects.all()
        courses = Course.objects.all()
        
        # Render the form with the list of available courses and students
        return render(request, 'teacher/publish_course.html', {'courses': courses, 'students': students})

def go_back1(request):
    return redirect('/teacher/teacher_exam')

def go_back(request):
    return redirect('/teacher/teacher_video')

