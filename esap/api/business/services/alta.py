"""
    File name: alta.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for ALTA.
"""

from .esap_service import esap_service
import requests, json
AMP_REPLACEMENT = '_and_'

# The request header
ALTA_HEADER = {
    'content-type': "application/json",
}


def alta_construct_query(url, dataset, esap_query_params, translation_parameters, equinox):
    """
    generic construct_query functionality for ALTA
    """
    query = ''
    where = ''
    error = None

    for esap_param in esap_query_params:
        esap_key = esap_param
        value = esap_query_params[esap_key][0]

        try:
            dataset_key = translation_parameters[esap_key]

            # because '&' has a special meaning in urls (specifying a parameter) replace it with
            # something harmless during serialization.
            where = where + dataset_key + '=' + value + AMP_REPLACEMENT

        except Exception as error:
            # if the parameter could not be translated, then just continue
            error = "ERROR: translating key " + esap_key + ' ' + str(error)
            return query, error

    # cut off the last separation character
    where = where[:-len(AMP_REPLACEMENT)]

    # construct the query url
    query = url + '?' + where

    return query, error


class observations_connector(esap_service):
    """
    The connector to access the ALTA observations dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        query, error = alta_construct_query(self.url, dataset, esap_query_params, translation_parameters, equinox)

        return query, error


    def run_query(self, dataset, query):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query: the constructed ALTA query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with the following structure;
        {
            "dataset": "astron.ivoa.obscore",
            "result": "https://vo.astron.nl/getproduct/tgssadr/fits/TGSSADR_R40D60_5x5.MOSAIC.FITS"
        },
        {
            "dataset": "astron.ivoa.obscore",
            "result": "https://vo.astron.nl/getproduct/tgssadr/fits/TGSSADR_R40D62_5x5.MOSAIC.FITS"
        },
        """
        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        # execute the http request to ALTA
        response = requests.request("GET", query, headers=ALTA_HEADER)

        try:
            json_response = json.loads(response.text)
            observations = json_response["results"]

            # iterate over the list of results
            for observation in observations:
                # the dataset.select_fields field specifies which fields must be extracted from the response
                record = {}
                result = ''

                select_list = dataset.select_fields.split(',')
                for select in select_list:
                    try:
                        result = result + observation[select] + ','
                    except:
                        pass

                # cut off the last ','
                result = result[:-1]

                result = "https://alta.astron.nl/science/details/"+observation["runId"]
                record['dataset'] = dataset.uri
                record['result'] = result
                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['result'] =  str(error)
            results.append(record)

        return results



class dataproducts_connector(esap_service):
    """
    The connector to access the ALTA dataproducts dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        query, error = alta_construct_query(self.url, dataset, esap_query_params, translation_parameters, equinox)

        return query, error


    def run_query(self, dataset, query):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query: the constructed ALTA query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with the following structure;
        {
            "dataset": "astron.ivoa.obscore",
            "result": "https://vo.astron.nl/getproduct/tgssadr/fits/TGSSADR_R40D60_5x5.MOSAIC.FITS"
        },
        {
            "dataset": "astron.ivoa.obscore",
            "result": "https://vo.astron.nl/getproduct/tgssadr/fits/TGSSADR_R40D62_5x5.MOSAIC.FITS"
        },
        """
        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        # execute the http request to ALTA
        response = requests.request("GET", query, headers=ALTA_HEADER)

        try:
            json_response = json.loads(response.text)
            observations = json_response["results"]

            # iterate over the list of results
            for observation in observations:
                # the dataset.select_fields field specifies which fields must be extracted from the response
                record = {}
                result = ''

                select_list = dataset.select_fields.split(',')
                for select in select_list:
                    try:
                        result = result + observation[select] + ','
                    except:
                        pass

                # cut off the last ','
                result = result[:-1]

                result = "https://alta.astron.nl/science/details/"+observation["runId"]
                record['dataset'] = dataset.uri
                record['result'] = result
                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['result'] =  str(error)
            results.append(record)

        return results