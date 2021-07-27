from django.views.generic import ListView
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions

from ida.models import Ida
from rest_framework import generics

from .serializers import IdaSerializer


class IdaViewSet(viewsets.ModelViewSet):
    serializer_class = IdaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.staging.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# example: /esap/ida/
class IndexView(ListView):
    queryset = Ida.objects.all()
    serializer_class = IdaSerializer
    template_name = 'ida/index.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_ida'


# example: /esap-api/ida/my_ida/
class StagingListViewAPI(generics.ListCreateAPIView):

    model = Ida
    queryset = Ida.objects.all()
    serializer_class = IdaSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = IdaFilter