from django.urls import path ,include
from cridential import views
from django.contrib import admin

from django.conf.urls.static import static



urlpatterns = [
    path("",views.home , name="home"),    
    path("register_user/",views.register_user , name="register_user"),
    path("show_all_user/",views.show_all_user ,name="show_all_user"),
    path('update_user_view/<int:pk>/', views.update_user_view, name='update_user_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users_delete/', views.delete_user, name='user_delete'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.custom_password_reset_confirm, name='reset_password'),
    




]

