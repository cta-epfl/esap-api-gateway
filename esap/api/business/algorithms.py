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
esap_parameters['esap_target'] = 'target__icontains'


@timeit
def prepare_query(datasets, esap_target):
    """
    Execute a query to a range of catalogs, using their catalog services
    :param query:
    :return:
    """
    logger.info('prepare_query : '+str(esap_target))
    query_input = []

    try:

        # iterate through the selected datasets
        for dataset in datasets:

            # per dataset, transate the common ESAP query parameters to the service specific parameters

            # build a result json structure for the input query
            input = {}
            input['dataset'] = dataset.uri

            try:
                input['service_url'] = str(dataset.dataset_catalog.url)
                parameters = dataset.dataset_catalog.parameters

                query = input['service_url'] + "?"
                # todo: add translation functionality
                if esap_target != None:
                    query = query + esap_parameters['esap_target'] + str(esap_target) + "&"

                input['query'] = query
                query_input.append(input)

            except Exception as error:
                input['service_url'] = str(error)


    except Exception as error:
        try:
            message = str(error.message)
            logger.error(message)
            return message
        except:
            return str(error)

    return query_input