import logging
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from rest_framework import generics, pagination, status

from rest_framework.views import APIView

from .models import Archive, DataSet
from .serializers import ArchiveSerializer, ArchiveModelSerializer, DataSetSerializer, DataSetModelSerializer

logger = logging.getLogger(__name__)


# ---------- REST API views -----------

# example: /esap-api/archives/
class ArchiveListViewAPI(generics.ListCreateAPIView):
    """
    A list of Archives
    """
    model = Archive
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


# example: /esap-api/archives/1/
class ArchiveDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of Archive
    """
    model = Archive
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    

class ArchiveListUriViewAPI(generics.ListCreateAPIView):
    """
    A list of Archives
    """
    model = Archive
    queryset = Archive.objects.all()
    serializer_class = ArchiveModelSerializer


# example: /esap-api-uri/archives/1/
class ArchiveDetailsUriViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of Archive
    """
    model = Archive
    queryset = Archive.objects.all()
    serializer_class = ArchiveModelSerializer


# example: /esap-api/datasets/
class DataSetListViewAPI(generics.ListCreateAPIView):
    """
    A list of DataSets
    """
    model = DataSet
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


# example: /esap-api/datasets/1/
class DataSetDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of DataSet
    """
    model = DataSet
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer


# example: /esap-api/datasets/
class DataSetListUriViewAPI(generics.ListCreateAPIView):
    """
    A list of DataSets
    """
    model = DataSet
    queryset = DataSet.objects.all()
    serializer_class = DataSetModelSerializer


# example: /esap-api/datasets/1/
class DataSetDetailsUriViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of DataSet
    """
    model = DataSet
    queryset = DataSet.objects.all()
    serializer_class = DataSetModelSerializer