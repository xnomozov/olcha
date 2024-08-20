"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView
from root import settings
from root import token_vieww
from root.token_vieww import LogoutView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('olcha-uz/', include('app.urls')),
                  path('api-token-auth/', token_vieww.CustomAuthToken.as_view()),
                  path('api/token/', token_vieww.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('login/', LogoutView.as_view(), name='token_blacklist'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += debug_toolbar_urls()
