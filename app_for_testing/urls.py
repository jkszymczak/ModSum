from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from register.views import (
    RegisterView,
    AccountView,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', include('product.urls')),
    path('account/', AccountView.as_view(), name='account'),
    path('', include('order.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)