from django.urls import path
from . import views

app_name = 'crypto'

urlpatterns = [
    path('crypto/history/', views.crypto_history_view, name="crypto_history"),
]