"""
    File name: query_controller.py
    Author: Nico Vermaas - Astron
    Date created: 2020-01-28
    Description:  Business logic for ESAP-gateway. These functions are called from the views (views.py).
"""

import importlib
import logging
import json
from .common import timeit

from .services.query import vo, alta, vso, helio, vo_reg

logger = logging.getLogger(__name__)

@timeit
def create_query(datasets, query_params):
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
                result['dataset'] = dataset.uri
                result['dataset_name'] = dataset.name
                try:
                    # get the url to the service for this dataset
                    result['service_url'] = str(dataset.dataset_catalog.url)
                    result['protocol'] = str(dataset.dataset_catalog.protocol)
                    result['esap_service'] = str(dataset.dataset_catalog.esap_service)
                    result['resource_name'] = str(dataset.resource_name)
                    result['output_format'] = str(dataset.output_format)
                    result['service_connector'] = str(dataset.service_connector)

                    # get the translation parameters for the service for this dataset
                    parameter_mapping = json.loads(dataset.dataset_catalog.parameters.parameters)

                    if parameter_mapping!=None:

                        # read the connector method to use from the dataset
                        service_module, service_connector = dataset.service_connector.split('.')

                        # distinguish between types of services to use
                        try:
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

                            url = str(dataset.dataset_catalog.url)
                            connector = connector_class(url)
                            query, errors = connector.construct_query(dataset, query_params, parameter_mapping,dataset.dataset_catalog.equinox)

                            result['query'] = query
                            if errors!=None:
                                result['remark'] = str(errors)

                        except Exception as error:
                            # connector not found
                            result["remark"] = str(error)
                            result["query"] = str(error)

                        # usually, the returned result in 'query' is a single query.
                        # occasionally, it is a structure of queries that was created by iterating over a registery
                        # if it is the latter, then add that structure to the input_results list.

                        if type(result["query"]) is list:
                            input_results.extend(result["query"])
                        else:
                            input_results.append(result)


                except Exception as error:
                    result["remark"] = str(error)
                    result['query'] = str(error)


    except Exception as error:
        try:
            message = str(error.message)
            logger.error(message)
            return message
        except:
            return str(error)

    return input_results



#@timeit
def run_query(dataset, dataset_name, query, access_url):
    """
    run a query on a dataset (catalog)
    :param query:
    :return:
    """
    logger.info('query_controller.run_query()')

    results = []

    # distinguish between types of services to use and run the query accordingly
    # query_base = dataset.dataset_catalog.query_base

    # read the connector method to use from the dataset
    service_module, service_connector = dataset.service_connector.split('.')

    # TODO: get import_module to work using both 'service_module' and 'service_connector' so that it can all be
    # TODO: done dynamically by reading the dataset. (then the query_base checks can be removed)
    # TODO: importlib.import_module('alta',package='services')

    try:
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

    except:
        # connector not found
        result = json.dumps({ "dataset" : dataset.uri, "result" : "ERROR: "+service_connector+" not found" })
        results = []
        results.append(result)
        return results

    # the default url to the catalog is defined in the dataset, but can be overridden.
    if access_url != None:
        my_url = access_url
    else:
        my_url = str(dataset.dataset_catalog.url)

    connector = connector_class(my_url)

    # run the specific instance of 'run_query' for this connector
    results = connector.run_query(dataset, dataset_name, query)
    return results