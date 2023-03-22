from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mtpass.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from pereval.views import *


router = routers.DefaultRouter()
router.register(r'pereval', PerevalViewSet)
router.register(r'coords', CoordsViewSet)
router.register(r'level', LevelViewSet)
router.register(r'user', UserViewSet)
router.register(r'images', ImagesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_api),
    path('pereval/', include('pereval.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/submitdata/', SubmitDataView.as_view(), name='submitdata'),
    path('api/v1/submitdata/<int:pk>/', SubmitDataView.as_view()),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


