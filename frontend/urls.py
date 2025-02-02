from django.urls import path
from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_user_view, name="sign_up"),
]