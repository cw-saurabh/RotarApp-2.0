from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('district/', admin.site.urls),
    path('', include('Main.urls')),
    path('', include('SecReport.urls')),
    path('', include('Auth.urls')),
    path('', include('DistReport.urls')),
]


if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
