from django.contrib import admin
from django.urls import path
from hiring import views
from hiring.views import show
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path, include


urlpatterns = [
    path("hiring_home/",views.home ,name="hiring_home"),
    path("admin/", admin.site.urls),
    path("edit1/<int:id>/" , views.edit1),
    path("update1/<int:id>/" , views.update1),
    path("detail_hr/<int:id>/" , views.detail_hr , name="detail_hr"),
    path("delete1/<int:id>/" , views.delete1),
    path("recruiter/",views.recruiter),
    path("show/",views.show ,name="show"),
    path('upload/', views.upload_file, name='resource_upload'),
    path('list/<int:job_id>/', views.view_files, name='resource_list'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('job/file_counts/', views.job_file_counts, name='job_file_counts'),
    path('share-files/', views.share_files, name='share_files'),
    path('company-data/', views.company_data, name='company_data'),
]


  