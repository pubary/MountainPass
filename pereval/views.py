from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import *


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


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesViewSerializer


class PerevalViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Added.objects.all()
    serializer_class = PerevalSerializer

    @action(methods=['post'], detail=False)
    def submitData(self, request):
        # try:
        #     serializer = SubmitDataSerializer(data=request.data)
        #     # parser_classes = (MultiPartParser, FormParser,)
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         pk = serializer.data['pk']
        #         return Response({'status': 200, 'message': None, 'id': pk})
        # except APIException as exc:
        #     if exc.status_code == 400:
        #         return Response({'status': exc.status_code, 'message': ' Bad Request', 'id': None})
        #     else:
        #         return Response({'status': exc.status_code, 'message': 'Ошибка подключения к базе данных', 'id': None})
        serializer = SubmitDataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            pk = serializer.data['pk']
            return Response({'status': 200, 'message': None, 'id': pk})


def redirect_to_api(request):
    return redirect('pereval/')

