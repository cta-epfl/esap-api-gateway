import logging

from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView

from rest_framework import generics


from django_filters import rest_framework as filters

from ..services import configuration

from query.models import Archive, DataSet, Catalog, ParameterMapping
from ..serializers import \
    ArchiveSerializer, \
    ArchiveModelSerializer, \
    DataSetSerializer, \
    DataSetModelSerializer, \
    CatalogSerializer, \
    ParameterMappingSerializer


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
    template_name = 'query/index.html'

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


def get_datasets():
    """
    The central function to get the datasets. It checks for configuration parameters.
    :return:
    """

    # first look if there are specifically enabled datasets
    try:
        datasets_enabled = configuration.get_datasets_enabled()
        datasets = DataSet.objects.filter(uri__in=datasets_enabled)
    except:
        # no specifically enabled datasets, so use all
        datasets = DataSet.objects.all()

    # then look if there are specifically disabled datasets to exclude.
    try:
        datasets_disabled = configuration.get_datasets_disabled()
        datasets = datasets.exclude(uri__in=datasets_disabled)
    except:
        # specifically disabled datasets, do not make a change in the datasets list
        pass

    return datasets


# example: /esap-api/datasets/
class DataSetListViewAPI(generics.ListCreateAPIView):
    """
    A list of DataSets
    """
    model = DataSet
    queryset = get_datasets()

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
    queryset = get_datasets()
    serializer_class = DataSetSerializer


# example: /esap-api/datasets/
class DataSetListUriViewAPI(generics.ListCreateAPIView):
    """
    A list of DataSets
    """
    model = DataSet
    queryset = get_datasets()

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
    queryset = get_datasets()
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


def ConfigurationView(request):
    """
    returns the configuration as a json object.
    The configuration is described in a file, which can be found by looking in the
    CONFIGURATION_FILE variable in the settings.py
    """

    try:
        config_from_settings = configuration.get_configuration()
    except:
        config_from_settings = "ERROR in configuration"

    return JsonResponse({'configuration': config_from_settings})


