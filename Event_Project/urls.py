"""Event_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ADMIN.views import AdminSettings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions 
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView

schema_view=get_schema_view(
    openapi.Info(
        title="E-TICKET API",
        description="E-TICKET API BUILT WITH DRF",
        default_version="v1",
        contact=openapi.Contact(email="maxstonne66@gmail.com"),
        public=True,
        
    ),
    permission_classes=[permissions.AllowAny]
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Events.urls')),
    path('', include('Users.urls')),
    path('', include('Transactions.urls')),
    path('admin-setting/', AdminSettings.as_view()),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('dj_rest_auth.urls')),
    path("password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('signup/', include('dj_rest_auth.registration.urls')),
       


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
