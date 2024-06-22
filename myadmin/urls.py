from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/register/', views.register_user_view, name='register_user'),
]