"""Actevia_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from onlinexam import views
from django.contrib.auth.views import LogoutView,LoginView
from cridential.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('student/',include('student.urls')),
    path('teacher/',include('teacher.urls')),
    path("contact/",include("contact.urls")),
    path("video/",include("postapp.urls")),
    path('asset/', include('assetapp.urls')),
    path('portal/resource/', include('employee_information.urls')),
    path('hiring/', include('hiring.urls')),
    path('policy/',include('myapp.urls')),
    path('cridential/',include('cridential.urls')),
    path('leave/',include('leaveapp.urls')),


    path("home/",views.home ,name="lms_home"),
    path("portal/",views.after_login_page, name="portal"),
    path("",login_view ,name="home_login"),
    path('admin_login/',views.admin_login , name="after_login_page"),
    path("admin_dashboard/" ,views.admin_dashboard),
    path("admin_logout",views.admin_logout ,name="admin_logout"),
    path("after_login/",views.after_login_view ,name="after_login_home"),
    path("admin_click_view/",views.admin_click_view ,name="admin_click_view"),


    path("admin_teacher/",views.admin_teacher),
    path("admin_teacher_view/",views.admin_teacher_view),
    path("admin_update_teacher/<int:pk>/",views.admin_update_teacher),
    path("admin_delete_teacher/<int:pk>/",views.admin_delete_teacher),

    path("admin_pending_teacher_view/",views.admin_pending_teacher_view),
    path("admin_approved_teacher_view/<int:pk>/",views.admin_approved_teacher_view),
    path("admin_reject_teacher_view/<int:pk>/",views.admin_reject_teacher_view),
    path("admin_teacher_salary_view/",views.admin_teacher_salary_view),


    path("admin_student/",views.admin_student),
    path("admin_view_student/",views.admin_view_student ,name="admin_view_student"),
    path("admin_update_student/<int:pk>/",views.admin_update_student),
    path("admin_delete_student/<int:pk>",views.admin_delete_student),
    
    


    path("admin_cource/",views.admin_cource),
    path("admin_add_cource/" ,views.admin_add_cource),
    path("admin_view_cource/",views.admin_view_cource),
    path("admin_delete_cource/<int:pk>/" ,views.admin_delete_cource),


    path("admin_questions/",views.admin_question),
    path("admin_add_question/",views.admin_add_questions),
    path("admin_view_question/",views.admin_view_questions),
    path("admin_view_question_set/<int:pk>/",views.admin_view_question_set),
    path("admin_delete_question/<int:pk>/",views.admin_delete_question),
    path("xl/",views.admin_add_question_xl),


    path("admin_view_student_marks/",views.admin_view_student_marks),
    path("admin_view_marks/<int:pk>/",views.admin_view_marks),
    path("admin_ckeck_marks/<int:pk>/",views.admin_check_marks),

    path("admin_video/",views.admin_video ,name="admin-video"),
    path("portal/collab/",views.collab),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
