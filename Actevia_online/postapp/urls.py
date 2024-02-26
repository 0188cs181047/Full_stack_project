"""postproject URL Configuration

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
from django.urls import path
from  . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('post/<int:pk>/', views.video_comments, name='video_comments'),
    path("see_video/",views.search ,name="see_video"),
    path("admin_see_video/<int:pk>/" ,views.admin_see_video ,name='admin_see_video'),
    path("detail_video/<int:pk>/",views.detail_video ,name="detail_video"),
    path("like/<int:pk>/",views.like ,name="like"),
    path("download/<int:pk>/",views.download_video ,name="download_video"),
    # path("share_video/<int:pk>/",views.share_video ,name="share_video"),
    path("delete_comment/<int:pk>/",views.delete_comment ,name="delete_comment"),
    path("reply_comment/<int:pk>/",views.reply_comment ,name="reply_comment"),
    path("view_video/",views.view_video ,name="view_video"),
    path("search/",views.search ,name="search"),
    path('qr_code/<int:pk>/', views.qr_code, name='qr_code'),
    path("home/",views.home ,name="home"),
    path("video_detail1/<int:pk>/",views.post_detail1 ,name="video_detail1"),
    path("create_video_form/",views.create_video_form , name="create_video-form"),
    path("update_video_form/<int:pk>/",views.update_video_form , name="update_video_form"),
    path("delete_video_form/<int:pk>/",views.delete_video_form , name="delete_video_form"),
    path("notfication/",views.notifications ,name="notification"),
    path('suggest_usernames/', views.suggest_usernames, name='suggest_usernames'),
    path("admin_create_video_form/",views.admin_create_video_form),
    path("admin_update_video_form/<int:pk>/",views.admin_update_video_form),
    path("admin_delete_video_form/<int:pk>/",views.admin_delete_video_form),
    path("admin_view_video/",views.admin_view_video),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


