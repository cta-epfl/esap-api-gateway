"""
    Business logic for ESAP-gateway.
    These functions are called from the 'views'.
"""

import json
import logging
from inspect import currentframe, getframeinfo

from . import apertif, astron_vo, ivoa, zooniverse, lofar, rucio, zenodo, concordia

logger = logging.getLogger(__name__)

def instantiate_connector(dataset):
    # read the connector method to use from the dataset
    service_module, service_connector = dataset.service_connector.split('.')

    # distinguish between types of services to use
    if service_module.upper() == 'ASTRON_VO':
        connector_class = getattr(astron_vo, service_connector)

    elif service_module.upper() == 'APERTIF':
        connector_class = getattr(apertif, service_connector)

    elif service_module.upper() == 'IVOA':
        connector_class = getattr(ivoa, service_connector)

    elif service_module.upper() == 'ZOONIVERSE':
        connector_class = getattr(zooniverse, service_connector)

    elif service_module.upper() == 'LOFAR':
        connector_class = getattr(lofar, service_connector)

    elif service_module.upper() == 'RUCIO':
        connector_class = getattr(rucio, service_connector)

    elif service_module.upper() == 'ZENODO':
        connector_class = getattr(zenodo, service_connector)

    elif service_module.upper() == 'CONCORDIA':
        connector_class = getattr(concordia, service_connector)

    url = str(dataset.dataset_catalog.url)
    connector = connector_class(url)
    return connector


def create_query(datasets, query_params, override_resource=None, connector=None, return_connector=False):
    """
    create a list of queries for a range of datasets, using their catalog services
    :param datasets:
    :return:
    """
    logger.info('query_controller.create_query()')
    input_results = []

    try:
        # iterate through the selected datasets
        # per dataset, transate the common esap query parameters to the service specific parameters

        for dataset in datasets:

            # check if there is a filter on institute, and if so, if the dataset is of the requested institute
            valid_institute = True
            if "institute" in query_params:
                if not dataset.institute in query_params['institute']:
                    valid_institute = False

            if valid_institute:
                # institute is valid, continue
                # build a result json structure for the input query
                result = {}
                result['query'] = "empty"
                result['error'] = []
                result['query_id'] = dataset.uri
                result['dataset'] = dataset.uri
                result['dataset_name'] = dataset.name
                try:
                    # get the url to the service for this dataset
                    result['service_url'] = str(dataset.dataset_catalog.url)
                    result['resource_name'] = str(dataset.resource_name)
                    result['output_format'] = str(dataset.output_format)
                    result['service_connector'] = str(dataset.service_connector)
                    result['res_description'] = dataset.short_description
                    result['reference_url'] = dataset.documentation_url

                    # Add some extra generic 'esap standard' fields that are also used
                    # in the 'query' endpoint. Used for some extra selection granularity
                    result['category'] = dataset.category
                    result['level'] = dataset.level
                    result['collection'] = dataset.collection

                    # get the translation parameters for the service for this dataset
                    parameter_mapping = json.loads(dataset.dataset_catalog.parameters.parameters)

                    if parameter_mapping is not None:
                        try:
                            if connector is None:
                                connector = instantiate_connector(dataset)

                            if override_resource:
                                query, where, errors = connector.construct_query(dataset,
                                                                                 query_params,
                                                                                 parameter_mapping,
                                                                                 override_resource)
                            else:
                                query, where, errors = connector.construct_query(dataset,
                                                                                 query_params,
                                                                                 parameter_mapping)
                            logger.info(query)
                            result['query'] = query
                            result['where'] = where

                            if errors is not None and len(errors):
                                result['error'].append(f"{getframeinfo(currentframe()).lineno}, {errors}")

                        except Exception as error:
                            # connector not found.
                            # store the error in the result and continue
                            result["error"].append(f"{getframeinfo(currentframe()).filename}, {getframeinfo(currentframe()).lineno}, {type(error)}, {error}")

                        # usually, the returned result in 'query' is a single query.
                        # occasionally, it is a structure of queries that was created by iterating over a registery
                        # if it is the latter, then add that structure to the input_results list.

                        if type(result["query"]) is list:
                            input_results.extend(result["query"])
                        else:
                            input_results.append(result)

                except Exception as error:
                    # store the error in the result and continue
                    result["error"].append(f"{getframeinfo(currentframe()).lineno}, {type(error)}, {error}")
                    input_results.append(result)

    except Exception as error:
        return "ERROR: " + str(error)

    if return_connector:
        return input_results, connector
    return input_results


def run_query(dataset,
              dataset_name,
              query,
              session=None,
              override_access_url=None,
              override_service_type=None,
              connector=None,
              return_connector=False):
    """
    run a query on a dataset (catalog)
    :param dataset: the dataset object that contains the information about the catalog to be queried
    :param query: the constructed (adql) query (that was probably generated with the above construct_query function)
    :param override_access_url: overrides access_url from the dataset
    :param override_service_type: overrides service_type from the dataset

    :return:
    """
    logger.info('query_controller.run_query()')
    results = []

    try:
        if connector is None:
            connector = instantiate_connector(dataset)
    except:
        # connector not found
        result = json.dumps({ "dataset" : dataset.uri, "result" : "ERROR: "+connector.__class__+" not found" })
        results = []
        results.append(result)
        return results

    # run the specific instance of 'run_query' for this connector
    results = connector.run_query(dataset, dataset_name, query, session, override_access_url, override_service_type)
    if return_connector:
        return results, connector
    return results

# when multiple queries are executed then the results must be combined.
def combine_results(data,data_to_add):
    logger.info('query_controller.combine_results()')
    if not data:
        data = data_to_add
        return data

    # if the data are a list, then just concatenate them.
    if isinstance(data, list):
        data = data + data_to_add

    # if the data are a (paginated) dict, then combine the totals and concatenate the data
    if isinstance(data, dict):
        count = int(data['count']) + int(data_to_add['count'])
        pages = int(data['pages']) + int(data_to_add['pages'])
        results = data['results'] + data_to_add['results']
        data['count']=count
        data['pages'] = pages
        data['results'] = results
    return data

# if the requested page_size spans multiple queries then adjust the page_size per query
def resize_page_size(query, new_page_size):
    # find 'page_size=' in the query

    logger.info('query_controller.resize_page_size('+str(new_page_size)+')')
    start = query.find("page_size=")

    if start >= 0:
        # find the next & or eol
        end = query.find("&",start)
        if end < 0:
            end = len(query)

        # replace the old page_size with the adjusted page_size
        old_page_size = query[start:end]
        new_page_size = "page_size="+str(new_page_size)
        query = query.replace(old_page_size,new_page_size)
    else:
        query = query + "page_size=" + str(new_page_size)

    return query


def create_and_run_query(datasets,
                         query_params,
                         override_resource,
                         override_access_url,
                         override_service_type,
                         override_adql_query,
                         session,
                         connector=None,
                         return_connector=False):
    """
    run a query on a list of datasets and return the results
    This function combines create_query and run_query
    :param query:
    :return:
    """
    logger.info("query_controller.create_and_run_query()")
    results = []
    created_queries = []
    if override_adql_query:
        q = {}
        # when a adql_query is given then there will also be only one dataset
        q['dataset'] = datasets[0].uri
        q['dataset_name'] = datasets[0].name
        q['query'] = override_adql_query
        created_queries.append(q)
    else:
        # call the 'create_query' function to construct a list of queries per dataset
        created_queries, connector = create_query(datasets, query_params, override_resource=override_resource, connector=connector, return_connector=True)

        # check if a "ERROR:" string was returned
        if "ERROR:" in created_queries:
            return created_queries, None

        # check if the returned dict contains an error
        try:
            if created_queries[0]['error']:
                error = created_queries[0]['error']
                if len(error)>2:
                    return error, None
        except:
            return "ERROR: could not create a query from these parameters"

    for q in created_queries:
        dataset_uri = q['dataset']
        dataset = datasets.get(uri=dataset_uri)

        dataset_name = q['dataset_name']
        query = q['query']

        try:
            connector = instantiate_connector(dataset)
        except:
            pass

        # the 'query' parameter from the 'create_query' function can be a bit richer than
        # what 'run_query' expects. This is the case for VO queries where a ADQL query is created.
        # When 'run_query' and 'create_query' are handled separately by a frontend then the
        # frontend ensures that the 'query' parameter is set.
        # In this combined 'query' function it must be done here
        try:
            query = query.split('&QUERY=')[1]
        except:
            pass

        # if 'create_query' gave back multiple queries to execute
        # then the requested page_size must be divided by the number of queries
        # so that the response still gives back the expected number of results

        nr_of_queries = len(created_queries)
        if nr_of_queries > 1:
            try:
                page_size = int(query_params['page_size'][0])
            except:
                page_size = 50
            new_page_size = int(page_size / nr_of_queries)
            query = resize_page_size(query, new_page_size)

        # call the 'run_query()' function to execute a query per dataset
        query_results = run_query(dataset, dataset_name, query,
                                  session=session,
                                  override_access_url=override_access_url,
                                  override_service_type=override_service_type,
                                  connector=connector,
                                  return_connector=False)

        if "ERROR:" in query_results:
            return query_results, None, None

        if nr_of_queries > 1:
            results = combine_results(results, query_results)
        else:
            results = query_results

        # attempt to retrieve a serializer for this function
        try:
            serializer = connector.CreateAndRunQuerySerializer
        except:
            serializer = None

    try:
        if return_connector:
            return results, connector, serializer
        return results, serializer
    except:
        if return_connector:
            return [], connector, None
        return [], None


def get_services(dataset, keyword, service_type=None, waveband=None):
    """

    :param dataset: dataset containing the link to the service_connector
    :param keyword: comma separated keywords
    :param service_type: TAP, SIA, SCS, SSA
    :param waveband: radio optical infrared uv euv nir gamma-ray x-ray

    :return:
    """
    logger.info("query_controller.get_services()")
    results = []

    try:
        connector = instantiate_connector(dataset)
    except:
        # connector not found
        result = json.dumps({ "dataset" : dataset.uri, "result" : "ERROR: "+connector.__class__+" not found" })
        results = []
        results.append(result)
        return results

    # run the specific instance of 'get_services' for this connector
    results = connector.get_services(service_type, waveband, keyword)

    return results


def get_tables_fields(dataset, access_url):
    """

    :param dataset: dataset containing the link to the service_connector
    :param access_url: access_url to the service to get the fields from

    :return:
    """
    logger.info("query_controller.get_tables_fields('+access_url+')")

    results = []

    try:
        connector = instantiate_connector(dataset)
    except:
        # connector not found
        result = json.dumps({ "dataset" : dataset.uri, "result" : "ERROR: "+connector.__class__+" not found" })
        results = []
        results.append(result)
        return results

    # run the specific instance of 'get_fields' for this connector
    results = connector.get_tables_fields(dataset, access_url)
    return results
