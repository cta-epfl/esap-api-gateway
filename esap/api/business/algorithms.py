"""
    File name: algorithms.py
    Author: Nico Vermaas - Astron
    Date created: 2020-01-28
    Description:  Business logic for ESAP-gateway. These functions are called from the views (views.py).
"""

import time
import datetime
import logging
import json
from .common import timeit

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M:%SZ"
DJANGO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

logger = logging.getLogger(__name__)

esap_parameters = {}
esap_parameters["esap_target"] = "target__icontains"


def construct_query(url, esap_query_params, translation_parameters, protocol):

    query = ''
    error = None

    for esap_param in esap_query_params:
        esap_key = esap_param
        value = esap_query_params[esap_key][0]

        try:
            dataset_key = translation_parameters[esap_key]

            # for the 'http' protocol glue the parameters together with &
            if protocol=='http':
                query = query + dataset_key + '=' + value + '&'

            if protocol=='adql':
                query = query + dataset_key + '=' + value + ' '

        except Exception as error:
            # if the parameter could not be translated, then just continue
            error = "ERROR: translating key " + esap_key + ' ' + str(error)
            return query,error

    # cut off the last separation character
    query = query[:-1]

    # construct the call
    if protocol == 'http':
        query = url + '?' + query

    elif protocol == 'adql':
        query = url + '&request=doQuery&lang=adql&query=' + query

    return query, error


@timeit
def prepare_query(datasets, query_params):
    """
    Execute a query to a range of catalogs, using their catalog services
    :param query:
    :return:
    """
    logger.info('prepare_query()')
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

                # get the translation parameters for the service for this dataset
                esap_translation_parameters = json.loads(dataset.dataset_catalog.parameters)

                if esap_parameters!=None:
                    query,error = construct_query(dataset.dataset_catalog.url, query_params, esap_translation_parameters,dataset.dataset_catalog.protocol)
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