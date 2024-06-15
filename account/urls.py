from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.login_user_view, name="login"),
    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('customer/get_data/', views.combined_data_view, name="combined_data_view"),
    path('customer/exchange/', views.exchange_view, name="exchange_view"),
    path('customer/wallet/', views.crypto_wallet_view, name="crypto_wallet_view"),
]