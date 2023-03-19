from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mtpass.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from pereval.views import redirect_to_api



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_api),
    path('pereval/', include('pereval.urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
