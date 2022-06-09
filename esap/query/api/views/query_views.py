import logging

from django.core.exceptions import FieldError
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from ..services import query_controller
from .. import utils
from query.models import DataSet

from ..query_serializers import (
    ServiceSerializer,
    TablesFieldSerializer,
    CreateAndRunQuerySerializer,
)

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


def no_datasets_found_error():
    error = "ERROR: No datasets found for this query. Check your 'dataset' configurations in the esap_config database"
    return Response({error})


def extract_and_filter(datasets, query_params, subject, filter_name, should_remove_query_param=True):
    if should_remove_query_param:
        query_params, subject_value = extract_and_remove(query_params, subject)
    else:
        try:
            subject_value = query_params[subject][0]
        except KeyError:
            subject_value = None

    if subject_value:
        try:
            # PEP 448 needed to use the filter field variable 'filter_name'
            datasets = datasets.filter(**{'{}__icontains'.format(filter_name): subject_value})
        except FieldError as error:
            raise FieldError(filter_name + " is not a known field for the Dataset object.\nError: " + str(error))

    return datasets, query_params


def filter_datasets(datasets, query_params):
    # the query will be run on all datasets that belong to the given archive_uri...
    # ...unless a dataset_uri is given, then it will only use that dataset
    datasets, query_params = extract_and_filter(datasets, query_params, "archive_uri", "dataset_archive__uri")
    if len(datasets) == 0:
        return datasets, query_params
    datasets, query_params = extract_and_filter(datasets, query_params, "dataset_uri", "uri")
    if len(datasets) == 0:
        return datasets, query_params

    # do not remove 'collection' from the query parameters since 'collection' is also a query parameter.
    # ... 'level' and 'category' are not
    datasets, query_params = extract_and_filter(datasets, query_params, "level", "level")
    if len(datasets) == 0:
        return datasets, query_params
    datasets, query_params = extract_and_filter(datasets, query_params, "category", "category")
    if len(datasets) == 0:
        return datasets, query_params
    datasets, query_params = extract_and_filter(datasets, query_params, "collection", "collection", False)

    return datasets, query_params


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

        datasets, query_params = filter_datasets(datasets, query_params)

        input_results = query_controller.create_query(
            datasets=datasets, query_params=query_params
        )

        return Response({"query_input": input_results})


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
        # datasets = DataSet.objects.all()

        # required parameters
        try:
            dataset_uri = self.request.query_params["dataset_uri"]
            query = self.request.query_params["query"]
            dataset = DataSet.objects.get(uri=dataset_uri)

        except Exception as error:
            return Response({"ERROR": str(error)})

        # optional parameters
        try:
            dataset_name = self.request.query_params["dataset_name"]
        except:
            dataset_name = "unknown"

        try:
            access_url = self.request.query_params["access_url"]
        except:
            access_url = "unknown"

        try:
            service_type = self.request.query_params["service_type"]
        except:
            service_type = "unknown"

        query_results = query_controller.run_query(
            dataset=dataset,
            dataset_name=dataset_name,
            query=query,
            override_access_url=access_url,
            override_service_type=service_type,
        )

        return Response({"results": query_results})


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

        session = request.session
        # token = session.get("oidc_access_token", None)

        datasets = common_views.get_datasets()
        query_params = dict(self.request.query_params)

        # if no query parameters given, the query should result in an error
        if len(query_params) == 0:
            error = "ERROR: No query parameters given. Needs at least an uri. " \
                    "Update your query to search for specific data"
            return Response({error})

        datasets, query_params = filter_datasets(datasets, query_params)

        if len(datasets) == 0:
            return no_datasets_found_error()

        query_params, access_url = extract_and_remove(query_params, "access_url")
        query_params, service_type = extract_and_remove(query_params, "service_type")
        query_params, adql_query = extract_and_remove(query_params, "adql_query")
        query_params, auto_pagination = extract_and_remove(query_params, "pagination")
        query_params, resource = extract_and_remove(query_params, "resource")

        query_results, connector, custom_serializer = query_controller.create_and_run_query(
            datasets=datasets,
            query_params=query_params,
            override_resource=resource,
            override_access_url=access_url,
            override_service_type=service_type,
            override_adql_query=adql_query,
            session=session,
            return_connector=True
        )

        if "ERROR:" in query_results or "Error" in query_results:
            return Response({query_results})

        # Allow pagination to be overriden by connector class
        auto_pagination = getattr(connector, "pagination", auto_pagination)

        # if the parameter 'pagination==false' is given, then do not automatically paginate the response
        # (currently this is only used by the zooniverse service)
        if auto_pagination is not None and auto_pagination.upper() == "FALSE":
            # pagination is implemented in the service connector

            # try to read the custom serializer from the controller...
            try:
                serializer = custom_serializer(instance=query_results, many=True)
            except:
                # ... if no serializer was implemented, then use the default serializer for this endpoint
                serializer = CreateAndRunQuerySerializer(
                    instance=query_results, many=True
                )

            # return the results with the custom or default serializer, but do not further paginate them.
            return Response({"results": serializer.data})

        else:
            # paginate the results
            if isinstance(query_results, dict):
                # if the query_results are a dict, then it is already in a paginated form.
                return Response(query_results)

            else:
                # the query_results are a list of results,
                # use a custom or default paginator to paginate and serialize them

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
            dataset_uri = self.request.query_params["dataset_uri"]
            dataset = DataSet.objects.get(uri=dataset_uri)
        except:
            return Response(
                {"error": "could not find 'dataset_uri' in the query_params"}
            )

        # find services that support his keyword
        keyword = request.GET.get('keyword', None)

        # if given, then only return services for this service_type
        service_type = None
        try:
            service_type = self.request.query_params["service_type"]
        except:
            logger.warning(
                "could not find 'service_type' in the query_params. Continuing..."
            )
            # give a warning and continue

        # if given, then only return services for this waveband
        waveband = None
        try:
            waveband = self.request.query_params["waveband"]
        except:
            logger.warning(
                "could not find 'waveband' in the query_params. Continuing..."
            )
            # give a warning and continue

        results = query_controller.get_services(
            dataset=dataset,
            service_type=service_type,
            waveband=waveband,
            keyword=keyword,
        )

        if "ERROR:" in results:
            return Response({results})

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
            dataset_uri = self.request.query_params["dataset_uri"]
            dataset = DataSet.objects.get(uri=dataset_uri)
        except:
            return Response(
                {"error": "could not find 'dataset_uri' in the query_params"}
            )

        # find services that support his keyword
        try:
            access_url = self.request.query_params["access_url"]
        except:
            return Response(
                {"error": "could not find 'access_url' in the query_params"}
            )

        results = query_controller.get_tables_fields(
            dataset=dataset, access_url=access_url
        )

        if "ERROR:" in results:
            return Response({results})

        # paginate the results
        page = self.paginate_queryset(results)
        serializer = TablesFieldSerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)


class GetSkyCoordinates(generics.ListAPIView):
    """
    Retrieve a list of fields from the access_url
    examples: /esap-api/query/get-sky-coordinates/?target_name=M31
    """

    model = DataSet
    queryset = DataSet.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        try:
            target_name = self.request.query_params["target_name"]
        except:
            return Response(
                {"error": "no target_name given"}
            )

        logger.info('GetSkyCoordinates(' + target_name + ')')
        target_coords = utils.get_sky_coords(target_name)
        print(target_coords)
        ra = target_coords.ra.deg
        dec = target_coords.dec.deg
        content = {
            'description': 'ICRS (ra, dec) in deg',
            'target_name': target_name,
            'ra': str(ra),
            'dec': str(dec)
        }

        return Response(content)
