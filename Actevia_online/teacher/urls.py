from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("teacher_home",views.Teacher_home),
    path("teacher_signUp/",views.teacher_signUp),
    path("teacher_signIn/",views.teacher_signIn ,name="teacher_signIn"),
    path("teacher_logout/",views.Teacher_logout),

    path("teacher_dashboard/",views.teacher_dashboard , name="teacher_dashboard"),

    path("teacher_exam/",views.teacher_exam),
    path("teacher_exam_add_cource/",views.teacher_add_exam_cource),
    path("teacher_view_exam_cource/",views.teacher_view_exam_cource),
    path("teacher_delete_exam_cource/<int:pk>/",views.teacher_delete_exam_cource),

    path("teacher_question/",views.teacher_question),
    path("teacher_add_question/",views.teacher_add_question),
    path("teacher_view_question/",views.teacher_view_question),
    path("teacher_see_question/<int:pk>/",views.teacher_see_question),
    path("teacher_delete_question/<int:pk>/",views.teacher_delete_question),
    path("teacher_xl_add_question/",views.teacher_xl_add_question),

    path("teacher_view_student_marks/",views.teacher_view_student_marks),
    path("teacher_view_marks/<int:pk>/",views.teacher_view_marks),
    path("teacher_check_marks/<int:pk>",views.teacher_check_marks),
    path("teacher_video/",views.teacher_video ,name="teacher_video"),
    path("publish_video/",views.teacher_publish ,name="publish_video"),
    path("publish_post/",views.publish_post , name="publish_post"),
    path('view_published_videos/<int:pk>/', views.view_published_videos, name='view_published_videos'),

    path('publish_course/', views.publish_course, name='publish_course'),
    path('go_back1/', views.go_back1, name='go_back1'),
    path('go_back/', views.go_back, name='go_back'),  
 

    
    
]