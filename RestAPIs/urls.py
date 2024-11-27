from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from blogs.views import BlogPostViewSet, RegisterUserViewSet, LoginUserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Constants
API_VERSION = 'api/v1/'
SWAGGER_PATH = 'swagger/'
REDOC_PATH = 'redoc/'

# Schema view setup
schema_view = get_schema_view(
    openapi.Info(
        title="Blogs API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amjidrafique786@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


# Router setup
router = DefaultRouter()
router.register('blogposts', BlogPostViewSet)

# URL patterns
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication URLs
    path(f'{API_VERSION}register/', RegisterUserViewSet.as_view(), name='register'),
    path(f'{API_VERSION}login/', LoginUserViewSet.as_view(), name='login'),

    # API route
    path(f'{API_VERSION}', include((router.urls, 'blogs'), namespace='blogs')),

    # Swagger and Redoc URLs
    path(f'{SWAGGER_PATH}', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{REDOC_PATH}', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
