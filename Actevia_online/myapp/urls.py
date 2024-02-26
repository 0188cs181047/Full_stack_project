from django.urls import path
from .views import policy_list, policy_new, policy_edit, policy_delete
from . import views

from django.conf.urls.static import static



app_name = 'myapp'
urlpatterns = [
    path("",views.home , name="home"),
    path('policy_list/', views.policy_list, name='policy_list'),
    path('policy_list2/', views.policy_list2, name='policy_list2'),
    path('new/', views.policy_new, name='policy_new'),
    path('edit/<int:pk>/', views.policy_edit, name='policy_edit'),
    path('policy_delete/',views. policy_delete, name='policy_delete'),
    path('policy_files/<int:pk>/', views.policy_files, name='policy_files'),
    path('new/<str:policy_name>/', views.policy_new, name='policy_new'),
    path('delete-file/<int:policy_pk>/<int:upload_pk>/', views.delete_file, name='delete_file')


]
