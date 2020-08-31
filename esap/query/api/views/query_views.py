import logging

from rest_framework import generics, pagination
from rest_framework.response import Response

from ..services import query_controller
from query.models import DataSet

from ..query_serializers import ServiceSerializer, TablesFieldSerializer, CreateAndRunQuerySerializer

from . import common_views

logger = logging.getLogger(__name__)


# extract a control parameter from the given list and then remove it from the list
# this is used to separate the control parameters from query parameters in the same url
def extract_and_remove(query_params, parameter):
    try:
        value = query_params[parameter][0]
        del query_params[parameter]
        return query_params, value
    except:
        # continue if the parameter was not found, they are usually not mandatory
        return query_params, None


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

        datasets = common_views.get_datasets()
        query_params = dict(self.request.query_params)

        # is there a query on archives?
        query_params,archive_uri = extract_and_remove(query_params, 'archive_uri')
        if archive_uri:
            datasets = datasets.filter(dataset_archive__uri=archive_uri)

        # is there a query on level?
        query_params, level = extract_and_remove(query_params, 'level')
        if level:
            datasets = datasets.filter(level=level)

        # is there a query on category?
        query_params, category = extract_and_remove(query_params, 'category')
        if category:
            datasets = datasets.filter(category=category)

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
                'ERROR': str(error)
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
    This function combines 'create-query' and 'run-query' in the 'query-controller'
    to be able to make a single request by the frontend, instead of 2 separate ones.

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
        query_params = dict(self.request.query_params)

        # the query will be run on all datasets that belong to the given archive_uri...
        query_params,archive_uri = extract_and_remove(query_params, 'archive_uri')
        if archive_uri:
            datasets = datasets.filter(dataset_archive__uri=archive_uri)

        # ...unless a dataset_uri is given, then it will only use that dataset
        query_params,dataset_uri = extract_and_remove(query_params, 'dataset_uri')
        if dataset_uri:
            datasets = datasets.filter(uri=dataset_uri)

        # is there a query on level?
        query_params, level = extract_and_remove(query_params, 'level')
        if level:
            datasets = datasets.filter(level=level)

        # is there a query on category?
        query_params, category = extract_and_remove(query_params, 'category')
        if category:
            datasets = datasets.filter(category=category)

        # is there a query on collection?
        try:
            collection = query_params['collection'][0]
            if collection:
                # do not remove 'collection' from the query parameters,
                # because (unlike 'level' and 'category') 'collection' is also a query parameter
                datasets = datasets.filter(collection=collection)
        except:
            pass

        query_params, access_url = extract_and_remove(query_params, 'access_url')
        query_params, service_type = extract_and_remove(query_params, 'service_type')
        query_params, adql_query = extract_and_remove(query_params, 'adql_query')
        query_params, pagination = extract_and_remove(query_params, 'pagination')

        query_results, custom_serializer = query_controller.create_and_run_query(
            datasets=datasets,
            query_params = query_params,
            override_access_url=access_url,
            override_service_type=service_type,
            override_adql_query=adql_query
        )

        if pagination.upper()=='FALSE':

            # try to read the custom serializer from the controller...
            try:
                serializer = custom_serializer(instance=query_results, many=True)
            except:
                # ... if no serializer was implemented, then use the default serializer for this endpoint
                serializer = CreateAndRunQuerySerializer(instance=query_results, many=True)

            return Response({
                'query_results': query_results
            })

        else:
            # paginate the results
            page = self.paginate_queryset(query_results)

            # try to read the custom serializer from the controller...
            try:
                serializer = custom_serializer(instance=page, many=True)
            except:
                # ... if no serializer was implemented, then use the default serializer for this endpoint
                serializer = CreateAndRunQuerySerializer(instance=page, many=True)

            return self.get_paginated_response(serializer.data)




class GetServices(generics.ListAPIView):
    """
    Retrieve a list of ivoa_services by keyword
    examples: /esap-api/query/get-services?dataset_uri=vo_reg&service_type=image&waveband=optical&keyword=UKIDSS
    """
    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

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
            keyword = None

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


class GetTablesFields(generics.ListAPIView):
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

        results = query_controller.get_tables_fields(dataset=dataset, access_url=access_url)

        if "ERROR:" in results:
              return Response({
                  results
            })

        # paginate the results
        page = self.paginate_queryset(results)
        serializer = TablesFieldSerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)

