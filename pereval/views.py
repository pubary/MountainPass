from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins, views
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
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


# class CoordsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
#     queryset = Coords.objects.all()
#     serializer_class = CoordsSerializer
#
#
# class LevelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
#     queryset = Level.objects.all()
#     serializer_class = LevelSerializer
#
#
# class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer
#
#
# class ImagesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
#     queryset = Images.objects.all()
#     serializer_class = ImagesSerializer


# class PerevalViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
#     queryset = Added.objects.all()
#     serializer_class = AddedSerializer
GET_EMAIL_RESP = 'sfwef'
GET_EMAIL_DISCR = 'efwegregrefq'
# @method_decorator(name='get', decorator=swagger_auto_schema(
#     manual_parameters=[
#         openapi.Parameter(
#             'user__email', openapi.IN_QUERY,
#             description=GET_EMAIL_DISCR,
#             type=openapi.FORMAT_EMAIL,
#             required=False
#         ),
#     ],
#     responses={'200': GET_EMAIL_RESP, }
# ))
class AddedView(views.APIView):
    @swagger_auto_schema(
            manual_parameters=[
            openapi.Parameter(
                'user__email', openapi.IN_QUERY,
                description=GET_EMAIL_DISCR,
                type=openapi.FORMAT_EMAIL,
                required=False
                ),
            ],
            responses={'200': GET_EMAIL_RESP, }
            )
    def get(self, request, *args, **kwargs):
        query = dict(self.request.GET.items())
        pk = kwargs.get('pk', None)
        if not pk:
            object = Added.objects.filter(**query)
            serializer = AddedSerializer(object, many=True)
        else:
            object = get_object_or_404(queryset=Added.objects.all(), pk=pk)
            serializer = AddedSerializer(object)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = AddedSerializer(data=request.data)
            parser_classes = (MultiPartParser, FormParser,)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                pk = serializer.data['id']
                return Response({'status': 200, 'message': None, 'id': pk})
        except APIException as exc:
            if exc.status_code == 400:
                return Response({'status': exc.status_code, 'message': 'Bad Request', 'id': None})
            else:
                return Response({'status': exc.status_code, 'message': 'Ошибка подключения к базе данных', 'id': None})

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'state': 0, 'message': 'Not id in Request'})
        try:
            instance = Added.objects.get(pk=pk)
        except:
            return Response({'state': 0, 'message': 'Object does not exists'})
        if instance.status == 'new':
            serializer = AddedSerializer(data=request.data, instance=instance)
            parser_classes = (MultiPartParser, FormParser,)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({'state': 1, 'message': 'Successfully'})
            except APIException as exc:
                return Response({'state': 0, 'message': f'Error {exc.detail}'})
        else:
            return Response({'state': 0, 'message': 'Forbidden to edit'})


def redirect_to_api(request):
    return redirect('pereval/')
