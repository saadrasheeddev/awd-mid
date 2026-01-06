# wineapi/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# For static files in production (Swagger needs this)
from django.conf import settings
from django.conf.urls.static import static

from api.views import WineViewSet

# Router for REST API endpoints
router = DefaultRouter()
router.register(r'wines', WineViewSet, basename='wine')

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Wine Quality API",
        default_version='v1',
        description="RESTful API for exploring the Wine Quality dataset (red & white wines)",
        contact=openapi.Contact(email="your.email@example.com"),
    ),
    public=True,
)

urlpatterns = [
    # Root URL shows Swagger UI
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Alternative docs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Django admin
    path('admin/', admin.site.urls),
]

# Static serving MUST be appended to urlpatterns (inside the file, after definition)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)