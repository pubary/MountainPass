from django.urls import path

from pereval.views import PerevalList, PerevalDetail

urlpatterns = [
    path('', PerevalList.as_view(template_name='perevals.html'), name='perevals'),
    path('<int:pk>', PerevalDetail.as_view(template_name='pereval.html'), name='pereval'),
]

