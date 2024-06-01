"""
URL configuration for config project.

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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# API documenting cinfigs
schema_view = get_schema_view(
    openapi.Info(
        title="FoxWeb API",
        default_version="v1",
        description="This is a FoxWeb api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mobin.ghanbarpour@yahoo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel url
    path("ckeditor5/", include("django_ckeditor_5.urls")),  # Ckeditor url
    path(
        "articles/api/v1/", include("articles_app.api.v1.urls")
    ),  # Article application urls
    path("accounts/api/v1/", include("users_app.api.v1.urls")),  # User application urls
    # Documentation urls
    path(
        "swagger/output.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),  # Download swagger output as .json file
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger endpoint
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),  # Redoc endpoint
    # JWT endpoints
    path("jwt/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("jwt/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns += urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
