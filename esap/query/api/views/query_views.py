import logging

from rest_framework import generics, pagination
from rest_framework.response import Response

from ..services import query_controller
from query.models import DataSet

from ..query_serializers import ServiceSerializer, TableFieldSerializer

from . import common_views

logger = logging.getLogger(__name__)

class CreateQueryView(generics.ListAPIView):
    """
    Receive a query and return the results
    examples:
    /esap-api/query/create-query/?esap_target=M51&archive_uri=astron_vo
    /esap-api/query/create-query/?ra=202&dec=46&fov=5
    """
    model = DataSet
    queryset = common_views.get_datasets()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        # read fields from the query

        datasets = common_views.get_datasets()

        # is there a query on archives?
        try:
            archive_uri = self.request.query_params['archive_uri']
            datasets = datasets.filter(dataset_archive__uri=archive_uri)

        except:
            pass

        # is there a query on level?
        try:
            level = self.request.query_params['level']
            datasets = datasets.filter(level=level)

        except:
            pass

        # is there a query on category?
        try:
            category = self.request.query_params['category']
            datasets = datasets.filter(category=category)

        except:
            pass

        # (remove the archive_uri (if present) from the params to prevent it being searched again
        query_params = dict(self.request.query_params)
        try:
            del query_params['archive_uri']
        except:
            pass

        try:
            del query_params['level']
        except:
            pass

        try:
            del query_params['category']
        except:
            pass

        input_results = query_controller.create_query(datasets=datasets, query_params = query_params)

        return Response({
            'query_input': input_results
        })


class RunQueryView(generics.ListAPIView):
    """
    Run a single query on a dataset (catalog) and return the results
    examples:
        /esap-api/query/run-query?dataset=ivoa.obscore&
        query=https://vo.astron.nl/__system__/tap/run/tap/sync?lang=ADQL&REQUEST=doQuery&
        QUERY=SELECT TOP 10 * from ivoa.obscore where target_name='M51'

        /esap-api/query/run-query/?dataset_uri=apertif_observations&query=https://alta.astron.nl/altapi/observations-flat?view_ra=202&view_dec=46&view_fov=5
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        # read fields from the query
        #datasets = DataSet.objects.all()

        # required parameters
        try:
            dataset_uri = self.request.query_params['dataset_uri']
            query = self.request.query_params['query']
            dataset = DataSet.objects.get(uri=dataset_uri)

        except Exception as error:
            return Response({
                'error': str(error)
            })


        # optional parameters
        try:
            dataset_name = self.request.query_params['dataset_name']
        except:
            dataset_name = "unknown"

        try:
            access_url = self.request.query_params['access_url']
        except:
            access_url = "unknown"

        try:
            service_type = self.request.query_params['service_type']
        except:
            service_type = "unknown"

        query_results = query_controller.run_query(dataset=dataset,
                                                   dataset_name=dataset_name,
                                                   query = query,
                                                   override_access_url = access_url,
                                                   override_service_type= service_type
                                                   )

        return Response({
            'query_results': query_results
        })


class CreateAndRunQueryView(generics.ListAPIView):
    """
    Run a single query on a series of datasets and return the results
    examples:
       /esap-api/query/query?level=raw&collection=imaging&ra=342.16&dec=33.94&fov=10&archive_uri=apertif
       /esap-api/query/query?level=raw&collection=timedomain&ra=342.16&dec=33.94&fov=10&archive_uri=apertif
       /esap-api/query/query?level=processed&collection=imaging&ra=342.16&dec=33.94&fov=10&archive_uri=apertif
       /esap-api/query/query?&collection=cutout&ra=342.16&dec=33.94&fov=10&archive_uri=astron_vo
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        datasets = common_views.get_datasets()

        # is there a query on archives?
        try:
            archive_uri = self.request.query_params['archive_uri']
            datasets = datasets.filter(dataset_archive__uri=archive_uri)
        except:
            pass

        # is there a query on level?
        try:
            level = self.request.query_params['level']
            datasets = datasets.filter(level=level)
        except:
            pass

        # is there a query on category?
        try:
            category = self.request.query_params['category']
            datasets = datasets.filter(category=category)
        except:
            pass

        # is there a query on collection?
        try:
            collection = self.request.query_params['collection']
            datasets = datasets.filter(collection=collection)
        except:
            pass

        # remove the dataset selection params, and keep the query search parameters
        query_params = dict(self.request.query_params)
        try:
            del query_params['archive_uri']
        except:
            pass

        try:
            del query_params['level']
        except:
            pass

        try:
            del query_params['category']
        except:
            pass

        # do not remove 'collection' from the query parameters, because (unlike 'level' and 'category')
        # 'collection' can be used as a parameter in the query itself.

        #try:
        #    del query_params['collection']
        #except:
        #    pass

        query_results = query_controller.create_and_run_query(datasets=datasets,query_params = query_params)

        return Response({
            'query_results': query_results
        })


class GetServices(generics.ListAPIView):
    """
    Retrieve a list of ivoa_services by keyword
    examples: /esap-api/query/get-services?dataset_uri=vo_reg&service_type=image&waveband=optical&keyword=UKIDSS
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        # datasets = common_views.get_datasets()

        # a dataset is needed to access a service_connector
        try:
            dataset_uri = self.request.query_params['dataset_uri']
            dataset = DataSet.objects.get(uri=dataset_uri)
        except:
            return Response({
                'error': "could not find 'dataset_uri' in the query_params"
            })

        # find services that support his keyword
        try:
            keyword = self.request.query_params['keyword']
        except:
            return Response({
                'error': "could not find 'keyword' in the query_params"
            })

        # if given, then only return services for this service_type
        service_type = None
        try:
            service_type = self.request.query_params['service_type']
        except:
            logger.warning("could not find 'service_type' in the query_params. Continuing...")
            # give a warning and continue

        # if given, then only return services for this waveband
        waveband = None
        try:
            waveband = self.request.query_params['waveband']
        except:
            logger.warning("could not find 'waveband' in the query_params. Continuing...")
            # give a warning and continue

        results = query_controller.get_services(dataset=dataset, service_type=service_type, waveband=waveband, keyword=keyword)

        if "ERROR:" in results:
              return Response({
                  results
            })

        # paginate the results
        page = self.paginate_queryset(results)
        serializer = ServiceSerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)


class GetTableFields(generics.ListAPIView):
    """
    Retrieve a list of fields from the access_url
    examples: /esap-api/query/get-fields?dataset_uri=vo_reg&access_url=https://vo.astron.nl/tap
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        datasets = common_views.get_datasets()

        # a dataset is needed to access a service_connector
        try:
            dataset_uri = self.request.query_params['dataset_uri']
            dataset = DataSet.objects.get(uri=dataset_uri)
        except:
            return Response({
                'error': "could not find 'dataset_uri' in the query_params"
            })

        # find services that support his keyword
        try:
            access_url = self.request.query_params['access_url']
        except:
            return Response({
                'error': "could not find 'access_url' in the query_params"
            })

        results = query_controller.get_table_fields(dataset=dataset, access_url=access_url)

        if "ERROR:" in results:
              return Response({
                  results
            })

        # paginate the results
        page = self.paginate_queryset(results)
        serializer = TableFieldSerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)

