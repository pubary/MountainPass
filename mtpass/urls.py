from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view as swagger_view

from mtpass.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from pereval.views import *


schema_view = swagger_view(
   openapi.Info(
      title="Pereval API",
      default_version='v1',
      description="API documentation of PaerevalApp",
      contact=openapi.Contact(email="contact@pereval.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_api),
    path('pereval/', include('pereval.urls')),
    # path('api/v1/', include(router.urls)),
    path('api/v1/submitdata/', AddedView.as_view(), name='submitdata'),
    path('api/v1/submitdata/<int:pk>/', AddedDetailView.as_view()),
    path('api/v1/swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


