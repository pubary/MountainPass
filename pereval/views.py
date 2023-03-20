from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from pereval.models import Added, Images
from pereval.serializers import PerevalSerializer, SubmitDataSerializer


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
    def submitData(self, request):
        try :
            serializer = SubmitDataSerializer(data=request.data)
            if serializer.is_valid():   #(raise_exception=True)
                serializer.save()
                pk = serializer.data['pk']
                return Response({'status': 200, 'message': None, 'id': pk})
            # else:
            #     return Response({'status': 400, 'message': ' Bad Request', 'id': None})
        except:
            return Response({'status': 500, 'message': 'Ошибка подключения к базе данных', 'id': None})




def redirect_to_api(request):
    return redirect('api/v1/')



