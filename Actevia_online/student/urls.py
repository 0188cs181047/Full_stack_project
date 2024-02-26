from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path("student_home/",views.student_home ,name="student_home"),
    path("thanks/",views.thank),
    path("student_signUp/",views.student_signUp),
    path("student_signIn/",views.Student_signIn ,name="student_signin"),
    path("student_logout/",views.student_logout),
    path("student_dashboard/",views.student_dashboard ,name="student_dashboard"),

    path("student_exam/",views.student_exam),
    path("student_take_exam/<int:pk>/",views.student_tack_exam),
    path("student_start_exam/<int:pk>/",views.student_start_exam),
    path('calculate_marks', views.calculate_marks_view ,name="calculate_marks"),

    path("student_view_result/",views.studetn_view_result),
    path("student_check_marks/<int:pk>/",views.student_view_check_marks),
    path("student_view_marks/",views.student_view_marks),
    path('student/published_course/<int:pk>/', views.view_published_courses, name='view_published_courses'),
    path('go_back1', views.go_back1, name='go_back1'),
    path("published_videos/<int:pk>/",views.show_video ,name="show_video"),
    

]