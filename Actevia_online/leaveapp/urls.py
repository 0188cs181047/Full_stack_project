"""
URL configuration for Leave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from leaveapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("leave_home/",views.home , name='leave_home'),
    path('manager_form/',views.manager_create, name = 'manager_form'),
    path("leave_manager_list/",views.leave_manager_list , name="leave_manager_list"),
    path('employee_create/', views.employee_create, name = 'employee_create'),
    path('leave_employee_list/', views.employee_list, name = 'leave_employee_list'),
    path("delete_selected_managers/",views.delete_selected_managers , name="delete_selected_managers"),
    path("update_manager/<int:pk>/",views.update_manager , name="update_manager"),
    path("delete_selected_employees/" ,views.delete_selected_employees , name="delete_selected_employees"),
    path("update_employee/<int:pk>/",views.update_employee , name="update_employee"),
    path("show_all_apply_leave/",views.show_all_apply_leave , name="show_all_apply_leave"),
    path("apply_leave_form/",views.apply_leave_form, name="apply_leave_form"),
    path("",views.profile,name="profile"),
    path("show_leave_balance/",views.show_leave_balance , name="show_leave_balance"),
    path("leave_approval/",views.leave_approval , name="leave_approval"),
    path("leave_balance_create/",views.leave_balance_create ,name="leave_balance_create"),
    path("my_holiday/",views.my_holiday , name="my_holiday"),
    path("create_holiday/",views.create_holiday , name="create_holiday"),
    path('reject_leave/', views.reject_leave, name='reject_leave'),
    path('apply_wfh_form/', views.apply_wfh_form, name='apply_wfh_form'),
    path('leave_balances/', views.leave_balance_view, name='leave_balances'),
    path("leave_balance_update/<int:pk>/",views.leave_balance_update , name='leave_balance_update'),
    path('leave_balance_delete/', views.leave_balance_delete, name='leave_balance_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

