"""
    File name: algorithms.py
    Author: Nico Vermaas - Astron
    Date created: 2020-01-28
    Description:  Business logic for ESAP-gateway. These functions are called from the views (views.py).
"""

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
                result['table_name'] = str(dataset.table_name)

                # get the translation parameters for the service for this dataset
                esap_translation_parameters = json.loads(dataset.dataset_catalog.parameters.parameters)

                if esap_translation_parameters!=None:

                    # distinguish between types of services to use
                    esap_service = dataset.dataset_catalog.esap_service
                    url = str(dataset.dataset_catalog.url)

                    if esap_service.upper()=='VO':
                        service = vo.tap_service_connector(url)

                    elif esap_service.upper()=='ALTA':
                        service = alta.observations_connector(url)

                    query, error = service.construct_query(dataset, query_params, esap_translation_parameters,dataset.dataset_catalog.equinox)

                    # query,error = construct_query(dataset.dataset_catalog.url, dataset.table_name, query_params, esap_translation_parameters,dataset.dataset_catalog.protocol)

                    result['query'] = query
                    if error!=None:
                        result['remark'] = error

                    input_results.append(result)

            except Exception as error:
                result['remark'] = str(error)
                if not 'url' in result['remark']: #skip the missing catalog errors for now, just missing content
                    input_results.append(result)


    except Exception as error:
        try:
            message = str(error.message)
            logger.error(message)
            return message
        except:
            return str(error)

    return input_results


@timeit
def run_query(dataset, query):
    """
    run a query on a dataset (catalog)
    :param query:
    :return:
    """
    logger.info('run_query()')

    results = []

    # distinguish between types of services to use and run the query accordingly
    esap_service = dataset.dataset_catalog.esap_service
    url = str(dataset.dataset_catalog.url)

    if esap_service.upper() == 'VO':
        service = vo.tap_service_connector(url)
        results = service.run_query(dataset, query)

    elif esap_service.upper() == 'ALTA':
        service = alta.alta_observation_service_connector(url)
        results = service.run_query(dataset, query)

    return results