
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('account/', include('account.urls', namespace="account")),
    path('stock/', include('stock.urls', namespace="stock")),
    path('crypto/', include('crypto.urls', namespace="crypto")),
]
