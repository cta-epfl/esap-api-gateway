"""
    File name: query_controller.py
    Author: Nico Vermaas - Astron
    Date created: 2020-01-28
    Description:  Business logic for ESAP-gateway. These functions are called from the views (views.py).
"""

import json
import logging

from . import alta
from . import vo, vso, helio, vo_reg, zooniverse
from ..utils import timeit

logger = logging.getLogger(__name__)

def instantiate_connector(dataset):
    # read the connector method to use from the dataset
    service_module, service_connector = dataset.service_connector.split('.')

    # distinguish between types of services to use
    if service_module.upper() == 'VO':
        connector_class = getattr(vo, service_connector)

    elif service_module.upper() == 'ALTA':
        connector_class = getattr(alta, service_connector)

    elif service_module.upper() == 'VSO':
        connector_class = getattr(vso, service_connector)

    elif service_module.upper() == 'HELIO':
        connector_class = getattr(helio, service_connector)

    elif service_module.upper() == 'VO_REG':
        connector_class = getattr(vo_reg, service_connector)

    elif service_module.upper() == 'ZOONIVERSE':
        connector_class = getattr(zooniverse, service_connector)

    url = str(dataset.dataset_catalog.url)
    connector = connector_class(url)
    return connector

#@timeit
def create_query(datasets, query_params, connector=None, return_connector=False):
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
                result['query_id'] = dataset.uri
                result['dataset'] = dataset.uri
                result['dataset_name'] = dataset.name
                try:
                    # get the url to the service for this dataset
                    result['service_url'] = str(dataset.dataset_catalog.url)
                    result['protocol'] = str(dataset.dataset_catalog.protocol)
                    result['resource_name'] = str(dataset.resource_name)
                    result['output_format'] = str(dataset.output_format)
                    result['service_connector'] = str(dataset.service_connector)
                    result['res_description'] = dataset.short_description
                    result['reference_url'] = dataset.documentation_url

                    # get the translation parameters for the service for this dataset
                    parameter_mapping = json.loads(dataset.dataset_catalog.parameters.parameters)

                    if parameter_mapping is not None:
                        try:
                            if connector is None:
                                connector = instantiate_connector(dataset)

                            query, where, errors = connector.construct_query(dataset, query_params, parameter_mapping,dataset.dataset_catalog.equinox)
                            result['query'] = query
                            result['where'] = where

                            if errors is not None:
                                result['error'] = str(errors)

                        except Exception as error:
                            # connector not found
                            result["error"] = str(error)

                        # usually, the returned result in 'query' is a single query.
                        # occasionally, it is a structure of queries that was created by iterating over a registery
                        # if it is the latter, then add that structure to the input_results list.

                        if type(result["query"]) is list:
                            input_results.extend(result["query"])
                        else:
                            input_results.append(result)

                except Exception as error:
                    result["error"] = str(error)
                    input_results.append(result)

    except Exception as error:
        try:
            message = str(error.message)
            logger.error(message)
            return message
        except Exception:
            return str(error)

    if return_connector:
        return input_results, connector
    return input_results

#@timeit
def run_query(dataset, dataset_name, query, access_url=None, connector=None, return_connector=False):
    """
    run a query on a dataset (catalog)
    :param query:
    :return:
    """
    results = []

    # distinguish between types of services to use and run the query accordingly
    # query_base = dataset.dataset_catalog.query_base
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
    results = connector.run_query(dataset, dataset_name, query)
    if return_connector:
        return results, connector
    return results


def create_and_run_query(datasets, query_params, connector=None, return_connector=False):
    """
    run a query on a list of datasets and return the results
    This function combines create_query and run_query
    :param query:
    :return:
    """

    results = []

    # call the 'create_query' function to construct a list of queries per dataset
    created_queries, connector = create_query(datasets, query_params, connector=connector, return_connector=True)

    for created_queries in created_queries:
        dataset_uri = created_queries['dataset']
        dataset = datasets.get(uri=dataset_uri)

        dataset_name = created_queries['dataset_name']
        # access_url = created_queries['service_url']
        query = created_queries['query']
        where = created_queries['where']

        # the 'query' parameter from the 'create_query' function can be a bit richer than
        # what 'run_query' expects. This is the case for VO queries where a ADQL query is created.
        # When 'run_query' and 'create_query' are handled separately by a frontend then the
        # frontend ensures that the 'query' parameter is.
        # In this combined 'query' function it must be done here
        try:
            query = query.split('&QUERY=')[1]
        except:
            pass

        # call the 'run_query()' function to execute a query per dataset
        query_results = run_query(dataset, dataset_name, query, connector=connector, return_connector=False)
        results = results + query_results

    try:
        if return_connector:
            return results, connector
        return results
    except:
        if return_connector:
            return [], connector
        return []
