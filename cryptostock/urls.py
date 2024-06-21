from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('account/', include('account.urls', namespace="account")),
    path('stock/', include('stock.urls', namespace="stock")),
    path('crypto/', include('crypto.urls', namespace="crypto")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
