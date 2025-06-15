from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as swagger_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static

schema_view = swagger_view(
    openapi.Info(
        title="ToDo API",
        default_version='v1',
        description="Simple Todo API with DRF",
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todo.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui') 
   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)