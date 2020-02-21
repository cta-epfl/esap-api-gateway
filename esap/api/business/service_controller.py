"""
    File name: algorithms.py
    Author: Nico Vermaas - Astron
    Date created: 2020-01-28
    Description:  Business logic for ESAP-gateway. These functions are called from the views (views.py).
"""

import importlib
import logging
import json
from .common import timeit

from .services import vo, alta

logger = logging.getLogger(__name__)

@timeit
def create_query(datasets, query_params):
    """
    create a query for a range of datasets, using their catalog services
    :param query:
    :return:
    """
    logger.info('create_query()')
    input_results = []

    try:

        # iterate through the selected datasets
        for dataset in datasets:

            # per dataset, transate the common esap query parameters to the service specific parameters

            # build a result json structure for the input query
            result = {}
            result['dataset'] = dataset.uri

            try:
                # get the url to the service for this dataset
                result['service_url'] = str(dataset.dataset_catalog.url)
                result['protocol'] = str(dataset.dataset_catalog.protocol)
                result['esap_service'] = str(dataset.dataset_catalog.esap_service)
                result['resource_name'] = str(dataset.resource_name)
                result['service_connector'] = str(dataset.service_connector)

                # get the translation parameters for the service for this dataset
                esap_translation_parameters = json.loads(dataset.dataset_catalog.parameters.parameters)

                if esap_translation_parameters!=None:

                    # read the connector method to use from the dataset
                    service_module, service_connector = dataset.service_connector.split('.')

                    # distinguish between types of services to use

                    try:
                        if service_module.upper() == 'VO':
                            connector_class = getattr(vo, service_connector)

                        elif service_module.upper() == 'ALTA':
                            connector_class = getattr(alta, service_connector)


                        url = str(dataset.dataset_catalog.url)
                        connector = connector_class(url)
                        query, errors = connector.construct_query(dataset, query_params, esap_translation_parameters,dataset.dataset_catalog.equinox)

                        result['query'] = query
                        if errors!=None:
                            result['remark'] = str(errors)

                    except Exception as error:
                        # connector not found
                        result["remark"] = str(error)
                        result["query"] = str(error)

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
def run_query(dataset, query):
    """
    run a query on a dataset (catalog)
    :param query:
    :return:
    """
    logger.info('run_query()')

    results = []

    # distinguish between types of services to use and run the query accordingly
    # esap_service = dataset.dataset_catalog.esap_service

    # read the connector method to use from the dataset
    service_module, service_connector = dataset.service_connector.split('.')

    # TODO: get import_module to work using both 'service_module' and 'service_connector' so that it can all be
    # TODO: done dynamically by reading the dataset. (then the esap_service checks can be removed)
    # TODO: importlib.import_module('alta',package='services')

    try:
        if service_module.upper() == 'VO':
            connector_class = getattr(vo, service_connector)

        elif service_module.upper() == 'ALTA':
            connector_class = getattr(alta, service_connector)

    except:
        # connector not found
        result = json.dumps({ "dataset" : dataset.uri, "result" : "ERROR: "+service_connector+" not found" })
        results = []
        results.append(result)
        return results

    url = str(dataset.dataset_catalog.url)
    connector = connector_class(url)

    # run the specific instance of 'run_query' for this connector
    results = connector.run_query(dataset, query)

    return results