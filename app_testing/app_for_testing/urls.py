from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from register.views import (
    RegisterView,
    AccountView,

)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('shop.urls'), name='shop'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', include('product.urls'), name='product'),
    path('account/', AccountView.as_view(), name='account'),
    path('', include('order.urls'), name='order'),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('product.api_urls'), name='api'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)