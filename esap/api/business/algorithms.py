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
import pyvo as vo

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M:%SZ"
DJANGO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

logger = logging.getLogger(__name__)

esap_parameters = {}
esap_parameters["esap_target"] = "target__icontains"


def construct_query(url, dataset_uri, esap_query_params, translation_parameters, protocol):

    query = ''
    clause = ''
    error = None

    for esap_param in esap_query_params:
        esap_key = esap_param
        value = esap_query_params[esap_key][0]

        try:
            dataset_key = translation_parameters[esap_key]

            # for the 'http' protocol glue the parameters together with &
            if protocol=='http':
                clause = clause + dataset_key + '=' + value + '&'

            if protocol=='adql':
                clause = clause + dataset_key + "='" + value + "' "

        except Exception as error:
            # if the parameter could not be translated, then just continue
            error = "ERROR: translating key " + esap_key + ' ' + str(error)
            return query,error

    # cut off the last separation character
    clause = clause[:-1]

    # construct the call
    if protocol == 'http':
        # example:
        # https://alta.astron.nl/altapi/observations-flat?target__icontains=M51

        query = url + '?' + clause

    elif protocol == 'adql':
        # example:
        # https://vo.astron.nl/__system__/tap/run/tap/sync/?lang=ADQL&REQUEST=doQuery&QUERY=SELECT TOP 10 * from ivoa.ObsCore

        # add sync (or async) specifier
        query = url + '/sync' \
        # query = url

        # add fixed ADQL parameters
        query = query + "?lang=ADQL&REQUEST=doQuery"

        # add query ADQL parameters (limit to 10 results)
        query = query + "&QUERY=SELECT TOP 10 * from "+dataset_uri

        # add ADQL where clause
        query = query + " where " + clause

    return query, error


@timeit
def create_query(datasets, query_params):
    """
    create a query to a range of catalogs, using their catalog services
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
                esap_translation_parameters = json.loads(dataset.dataset_catalog.parameters.parameters)

                if esap_parameters!=None:
                    query,error = construct_query(dataset.dataset_catalog.url, dataset.uri, query_params, esap_translation_parameters,dataset.dataset_catalog.protocol)
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



def do_vo_query(url,query):
    """
    # use pyvo to do a vo query
    :param url: acces url of the vo service
    :param query: adql query
    :return:
    """

    # use pyvo the get to the results
    service = vo.dal.TAPService(url)
    resultset = service.search(query)

    for row in resultset:
        # for the definition of standard fiels to return see:
        # http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf
        obs_title = row["obs_title"].decode('utf-8')
        access_url = row["access_url"].decode('utf-8')

    print(obs_title,access_url)
    return obs_title, access_url

@timeit
def run_query(dataset, query):
    """
    run a query on a dataset (catalog)
    :param query:
    :return:
    """
    logger.info('run_query()')

    query_result = {}
    query_result['dataset_uri'] = dataset.uri
    urls = []

    protocol = str(dataset.dataset_catalog.protocol)

    # check for VO query
    if protocol.upper() == 'ADQL':
        url = str(dataset.dataset_catalog.url)
        obs_name, access_url = do_vo_query(url,query)
        # query_result['response'] = str(response)
        urls.append(access_url)

    else:
        # none VO queries (ALTA)
        try:
            urls.append(query)

        except Exception as error:
            try:
                message = str(error.message)
                logger.error(message)
                return message
            except:
                return str(error)

    query_result['urls'] = urls
    return query_result