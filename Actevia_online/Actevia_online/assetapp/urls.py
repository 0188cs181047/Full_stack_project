from django.urls import path, include
from assetapp import views

urlpatterns = [
    path("",views.before_login ,name="befor_login"),
    path("asset_detail/",views.Asset_detail , name="asset_detail"),
    path("create_asset/",views.create_asset ,name="create_asset"),
    path("update_asset/<int:pk>/",views.Updata_asset ,name="update_asset"),
    path("delete_asset/<int:pk>/",views.Delete_asset ,name="delete_asset"),
    #path("asset_filter/",views.asset_list ,name="asset_filter"),
    path('view_asset/<int:pk>/', views.view_asset, name='view_asset'),
    path('qr_code_asset/<int:pk>/',views.qr_code_asset , name="qr_asset"),
    path('export-assets-to-excel/', views.export_assets_to_excel, name='export_assets_to_excel'),
   
]

