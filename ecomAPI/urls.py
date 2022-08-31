"""ecomAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_yasg.views import get_schema_view as gs
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from dj_rest_auth.views import PasswordResetConfirmView

schema_view = gs(
	openapi.Info(
		title="Irish API",
		default_version='1.0.0',
		description="API doc for Irish API",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="ugahchymdy@gmail.com"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
	# path('user/')
	path('', include('irish.urls')),
	path('users/socaccounts/', include('allauth.urls')),
	path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('openapi/', get_schema_view(
		title="Irish API",
		description="API doc for Irish API",
		permission_classes=[permissions.AllowAny],
		version='1.0.0',
	), name='openapi-schema'),
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
