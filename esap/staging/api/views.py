from django.views.generic import ListView
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions

from staging.models import Staging
from rest_framework import generics

from .serializers import StagingSerializer


class StagingViewSet(viewsets.ModelViewSet):
    serializer_class = StagingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.staging.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# example: /esap/query/
class IndexView(ListView):
    queryset = Staging.objects.all()
    serializer_class = StagingSerializer
    template_name = 'staging/index.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_staging'

# example: /esap-api/staging/staging/
class StagingListViewAPI(generics.ListCreateAPIView):
    """
    A list of Archives
    """
    model = Staging
    queryset = Staging.objects.all()
    serializer_class = StagingSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = StagingFilter