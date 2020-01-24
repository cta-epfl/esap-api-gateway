import logging
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from rest_framework import generics, pagination, status

from rest_framework.views import APIView
from django_filters import rest_framework as filters

from .models import Archive, DataSet, Catalog, CatalogService, RetrievalParameters
from .serializers import \
    ArchiveSerializer, \
    ArchiveModelSerializer, \
    DataSetSerializer, \
    DataSetModelSerializer, \
    CatalogSerializer, \
    CatalogServiceSerializer, \
    RetrievalParametersSerializer

logger = logging.getLogger(__name__)

# ---------- REST API filters -----------

class ArchiveFilter(filters.FilterSet):

    class Meta:
        model = Archive

        fields = {
            'name': ['exact', 'in', 'icontains'],
            'long_description': ['icontains'],
            'institute': ['exact', 'in', 'icontains'],
        }


class DataSetFilter(filters.FilterSet):
    class Meta:
        model = DataSet

        fields = {
            'name': ['exact', 'in', 'icontains'],
            'long_description': ['icontains'],
            'institute': ['exact', 'in', 'icontains'],
            # example: select DataSets from archive with uri 'astron_vo':
            # /esap-api/datasets-uri/?data_archive__uri=astron_vo
            'data_archive__uri': ['exact', 'in', 'icontains'],
        }


class CatalogFilter(filters.FilterSet):
    class Meta:
        model = Catalog

        fields = {
            'name': ['exact', 'in', 'icontains'],
            'long_description': ['icontains'],
            'institute': ['exact', 'in', 'icontains'],
        }


class CatalogServiceFilter(filters.FilterSet):
    class Meta:
        model = CatalogService

        fields = {
            'name': ['exact', 'in', 'icontains'],
            'long_description': ['icontains'],
            'institute': ['exact', 'in', 'icontains'],
        }


class RetrievalParametersFilter(filters.FilterSet):
    class Meta:
        model = RetrievalParameters

        fields = {
            'service__uri': ['exact', 'in', 'icontains'],
            'input_parameter': ['exact', 'in', 'icontains'],
            'input_operator': ['exact', 'in', 'icontains'],
            'output_parameter': ['exact', 'in', 'icontains'],
            'output_operator': ['exact', 'in', 'icontains'],

        }


# ---------- REST API views -----------

# example: /esap-api/archives/
class ArchiveListViewAPI(generics.ListCreateAPIView):
    """
    A list of Archives
    """
    model = Archive
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ArchiveFilter


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

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = DataSetFilter


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

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = DataSetFilter


# example: /esap-api/datasets/1/
class DataSetDetailsUriViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of DataSet
    """
    model = DataSet
    queryset = DataSet.objects.all()
    serializer_class = DataSetModelSerializer


# example: /esap-api/catalogs/
class CatalogListViewAPI(generics.ListCreateAPIView):
    """
    A list of Catalogs
    """
    model = Catalog
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CatalogFilter


# example: /esap-api/catalogs/1/
class CatalogDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of Catalog
    """
    model = Catalog
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


# example: /esap-api/catalog-services/
class CatalogServicesListViewAPI(generics.ListCreateAPIView):
    """
    A list of CatalogServices
    """
    model = CatalogService
    queryset = CatalogService.objects.all()
    serializer_class = CatalogServiceSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CatalogServiceFilter


# example: /esap-api/catalog-services/1/
class CatalogServicesDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Detailed view of CatalogService
    """
    model = CatalogService
    queryset = CatalogService.objects.all()
    serializer_class = CatalogServiceSerializer


# example: /esap-api/retrieval-parameters/
class RetrievalParametersListViewAPI(generics.ListCreateAPIView):
    """
    A list of Retrieval Parameters per service
    """
    model = RetrievalParameters
    queryset = RetrievalParameters.objects.all()
    serializer_class = RetrievalParametersSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RetrievalParametersFilter


# example: /esap-api/retrieval-parameters/1
class RetrievalParametersDetailsViewAPI(generics.ListCreateAPIView):
    """
    Details for Retrieval Parameters for a service
    """
    model = RetrievalParameters
    queryset = RetrievalParameters.objects.all()
    serializer_class = RetrievalParametersSerializer
