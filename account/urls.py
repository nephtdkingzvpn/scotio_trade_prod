from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.login_user_view, name="login"),
    path('customer/dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('customer/get_data/', views.combined_data_view, name="combined_data_view"),
    path('customer/exchange/', views.exchange_view, name="exchange_view"),
    path('customer/exchange/c-to-d/', views.exchange_crypto_tousd_view, name="exchange_crypto_tousd"),
    path('customer/wallet/', views.crypto_wallet_view, name="crypto_wallet_view"),
    path('customer/account/', views.list_bank_accounts_view, name="list_bank_account"),
    path('customer/add/account/', views.add_new_account_view, name="add_new_account"),
    path('customer/account/<pk>/delete/', views.delete_account_view, name="delete_account"),
    path('customer/withdraw/<pk>/', views.withdraw_dollars_view, name="withdraw_dollars"),

    # get crypto price history
    path('crypto-price-history/', views.crypto_price_history, name='crypto_price_history'),
]