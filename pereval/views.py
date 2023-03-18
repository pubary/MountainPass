from django.views.generic import ListView, DetailView

from pereval.models import Added, Images


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



