from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import views
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .serializers import *


PATCH_RESPONSES = {'200': '{"state": 1, "message": "Successfully"}',
                  'other exc.': '{"state": 1, "message": "Error {exc.detail}"}',
                  'when obj.status not "new"': '{"state": 0, "message": "Forbidden to edit"}'}

POST_RESPONSES = {'200': '{"status": 200, "message": null, "id": id }',
                  '400': '{ "status": 400, "message": "Bad Request", "id": None}',
                  '500': '{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}}'}

GET_EMAIL_DISCR = f"You can enter user's email to display his sending"


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


class AddedView(views.APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('user__email',
                                openapi.IN_QUERY, description=GET_EMAIL_DISCR,
                                required=False, type=openapi.FORMAT_EMAIL),],
        responses={'200': AddedSerializer, }, )
    def get(self, request, **kwargs):
        query = dict(self.request.GET.items())
        object = Added.objects.filter(**query)
        serializer = AddedSerializer(object, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses=POST_RESPONSES, request_body=AddedSerializer, )
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


class AddedDetailView(views.APIView):
    @swagger_auto_schema(responses={'200': AddedSerializer, }, )
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        object = get_object_or_404(queryset=Added.objects.all(), pk=pk)
        serializer = AddedSerializer(object)
        return Response(serializer.data)

    @swagger_auto_schema(responses=PATCH_RESPONSES, request_body=AddedSerializer, )
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

