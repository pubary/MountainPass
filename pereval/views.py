from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pereval.models import Added, Images
from pereval.serializers import PerevalSerializer


class PerevalList(ListView):
    model = Added
    ordering = 'title'
    context_object_name = 'perevals'
    extra_context = {'title': 'Перевалы'}


class PerevalDetail(DetailView):
    model = Added
    context_object_name = 'pereval'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Images.objects.filter(pereval__pk=self.kwargs['pk'])
        context['images'] = images
        return context


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Added.objects.all()
    serializer_class = PerevalSerializer

    @action(methods=['post'], detail=False)
    def submitData(self, request, pk=None):
        print(request.data['user'])
        # pereval = Added.objects.get(pk=pk)
        return Response({'id': '123'})




def redirect_to_api(request):
    return redirect('api/v1/')
