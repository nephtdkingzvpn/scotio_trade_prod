from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/register/', views.register_user_view, name='register_user'),
    path('admin/edit/<pk>/customer/', views.edit_user_view, name='edit_user'),
    path('admin/delete/<pk>/customer/', views.delete_user_view, name='delete_user'),
    path('admin/detail/<pk>/customer/', views.detail_user_view, name='detail_user'),
]