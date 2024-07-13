from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('list/stock/', views.stock_list_view, name="stock_list"),
    path('buy/stock/', views.buy_new_stock_view, name="buy_new_stock"),
    path('sell/stock/', views.sell_stock_view, name="sell_stock"),
    path('history/stock/', views.stock_trade_history_view, name="stock_trade_history"),
]