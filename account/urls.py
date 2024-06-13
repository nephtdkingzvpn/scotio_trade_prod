from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.login_user_view, name="login"),
    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('customer/get_data/', views.aapl_data_view, name="aapl_data_view"),
]