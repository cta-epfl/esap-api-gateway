import logging
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from rest_framework import generics, pagination, status

from rest_framework.views import APIView


from .models import DataSource
from .serializers import DataSourceSerializer

logger = logging.getLogger(__name__)


# ---------- REST API views -----------

# example: /adex/datasources/
class DataSourceListViewAPI(generics.ListCreateAPIView):
    """
    A list of datasources
    """
    model = DataSource
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer


# example: /adex/datasources/1/
class DataSourceDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of datasource
    """
    model = DataSource
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

