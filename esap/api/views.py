import logging
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from rest_framework import generics, pagination, status
from rest_framework.response import Response

from rest_framework.views import APIView
from django_filters import rest_framework as filters

from .models import Archive, DataSet, Catalog, ParameterMapping
from .serializers import \
    ArchiveSerializer, \
    ArchiveModelSerializer, \
    DataSetSerializer, \
    DataSetModelSerializer, \
    CatalogSerializer, \
    ParameterMappingSerializer

from .business import service_controller

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
            # /esap-api/datasets-uri/?dataset_archive__uri=astron_vo
            'dataset_archive__uri': ['exact', 'in', 'icontains'],
            'dataset_catalog__uri': ['exact', 'in', 'icontains'],
        }


class CatalogFilter(filters.FilterSet):
    class Meta:
        model = Catalog

        fields = {
            'name': ['exact', 'in', 'icontains'],
            'long_description': ['icontains'],
            'institute': ['exact', 'in', 'icontains'],
            'url': ['exact', 'in', 'icontains'],
        }


class ParameterMappingFilter(filters.FilterSet):
    class Meta:
        model = ParameterMapping

        fields = {
            'uri': ['exact', 'in', 'icontains'],
            'parameters': ['icontains'],
        }


# ---------- REST API views -----------

# example: /my_energy
class IndexView(ListView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    template_name = 'api/index.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_archives'


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



# example: /esap-api/retrieval-parameters/
class ParameterMappingListViewAPI(generics.ListCreateAPIView):
    """
    A list of Retrieval Parameters per service
    """
    model = ParameterMapping
    queryset = ParameterMapping.objects.all()
    serializer_class = ParameterMappingSerializer

    # using the Django Filter Backend - https://django-filter.readthedocs.io/en/latest/index.html
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ParameterMappingFilter


# example: /esap-api/retrieval-parameters/1
class ParameterMappingDetailsViewAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Details for Retrieval Parameters for a service
    """
    model = ParameterMapping
    queryset = ParameterMapping.objects.all()
    serializer_class = ParameterMappingSerializer


class CreateQueryView(generics.ListAPIView):
    """
    Receive a query and return the results
    examples:
    /esap-api/create-query/?esap_target=M51&archive_uri=astron_vo
    /esap-api/create-query/?ra=202&dec=46&fov=5
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        # read fields from the query

        datasets = DataSet.objects.all()

        # is there a query on archives?
        try:
            archive_uri = self.request.query_params['archive_uri']
            datasets = datasets.filter(dataset_archive__uri=archive_uri)

        except:
            pass

        # (remove the archive_uri (if present) from the params to prevent it being searched again
        query_params = dict(self.request.query_params)
        try:
            del query_params['archive_uri']
        except:
            pass

        input_results = service_controller.create_query(datasets=datasets, query_params = query_params)

        return Response({
            'query_input': input_results
        })


class RunQueryView(generics.ListAPIView):
    """
    Run a single query on a dataset (catalog) and return the results
    examples:
        /esap-api/run-query?dataset=ivoa.obscore&
        query=https://vo.astron.nl/__system__/tap/run/tap/sync?lang=ADQL&REQUEST=doQuery&
        QUERY=SELECT TOP 10 * from ivoa.obscore where target_name='M51'

        /esap-api/run-query/?dataset_uri=apertif_observations&query=https://alta.astron.nl/altapi/observations-flat?view_ra=202&view_dec=46&view_fov=5
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        # read fields from the query
        #datasets = DataSet.objects.all()

        # is there a query on archives?
        try:
            dataset_uri = self.request.query_params['dataset_uri']
            query = self.request.query_params['query']
            dataset = DataSet.objects.get(uri=dataset_uri)

        except Exception as error:
            return Response({
                'error': str(error)
            })

        query_results = service_controller.run_query(dataset=dataset, query = query)

        return Response({
            'query_results': query_results
        })
