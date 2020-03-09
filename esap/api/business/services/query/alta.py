"""
    File name: alta.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for ALTA.
"""

from .query_base import query_base
import requests, json
AMP_REPLACEMENT = '_and_'

# The request header
ALTA_HEADER = {
    'content-type': "application/json",
}


class observations_connector(query_base):
    """
    The connector to access the ALTA observations dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        query = ''
        where = ''
        errors = []

        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, then just continue without that key
                errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # cut off the last separation character
        where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url
        query = self.url + '?' + where

        return query, errors


    def run_query(self, dataset, query):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query: the constructed ALTA query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with the following structure;

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

                #result = "https://alta.astron.nl/science/details/"+observation["runId"]
                record['dataset'] = dataset.uri
                record['result'] = result

                # some fields to return some rendering information for the frontend.
                try:
                    record['title'] = observation[dataset.title_field]
                except:
                    pass

                try:
                    record['thumbnail'] = observation[dataset.thumbnail_field]
                except:
                    pass

                try:
                    record['url'] = "https://alta.astron.nl/science/details/"+observation["runId"]
                except:
                    pass

                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['result'] =  str(error)
            results.append(record)

        return results


# --------------------------------------------------------------------------------------------------------------------

class dataproducts_connector(query_base):
    """
    The connector to access the ALTA dataproducts dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url


    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

        query = ''
        where = ''
        errors = []

        # add some weird business logic for the ALTA dataproducts query, which cannot really do a cone search

        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, then just continue without this parameter
                errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # cut off the last separation character
        where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url
        query = self.url + '?' + where

        return query, errors



    def run_query(self, dataset, query):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query: the constructed ALTA query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with the following structure;

        {
            "dataset": "apertif-dataproducts",
            "result": "/alta-static//media/190409015_AP_B000/image_mf_02.png"
        },
        {
            "dataset": "apertif-dataproducts",
            "result": "/alta-static//media/190409015_AP_B001/image_mf_02.png"
        },
        {
            "dataset": "apertif-dataproducts",
            "result": "/alta-static//media/190409015_AP_B002/image_mf_02.png"
        },
        {
            "dataset": "apertif-dataproducts",
            "result": "/alta-static//media/190409015_AP_B003/image_mf_01.png"
        },

        example:
        /esap-api/run-query/?dataset_uri=apertif-dataproducts&query=https://alta.astron.nl/altapi/observations-flat?view_ra=342.16_and_view_dec=33.94_and_view_fov=10_and_dataProductType=image_and_dataProductSubType=continuumMF

        """
        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        try:

            # execute the first http request to ALTA to do the cone search on observation level.
            response = requests.request("GET", query, headers=ALTA_HEADER)

            json_response = json.loads(response.text)
            observations = json_response["results"]

            # iterate over the list of results.. and gather the runid's in a comma separated list for the next query on datasetid
            list = []
            for observation in observations:
                list.append(observation['runId'])

            runids = ','.join(list)

            # construct a second query on dataproducts for the gathered runId's
            query_list = query.split('/observations')
            host = query_list[0]

            # there may be additional query parameters in the original query, like dataProductSubType=continuumMF
            # copy them over to the secondary query as well.
            filter = '&'+query_list[1].split('?')[1]
            query2 = host + '/dataproducts-flat?datasetID__in=' + str(runids) + filter

            # shortcut to add an extra selection criterium... handle better later
            # query2 = query2 + "&dataProductSubType=continuumMF"

            # execute the secondary query to dataproducts
            response = requests.request("GET", query2, headers=ALTA_HEADER)

            json_response = json.loads(response.text)
            dataproducts = json_response["results"]


            for dataproduct in dataproducts:
                # the dataset.select_fields field specifies which fields must be extracted from the response
                record = {}
                result = ''

                select_list = dataset.select_fields.split(',')
                for select in select_list:
                    try:
                        result = result + dataproduct[select] + ','
                    except:
                        pass

                # cut off the last ','
                result = result[:-1]

                # result = "https://alta.astron.nl/science/details/"+observation["runId"]
                record['dataset'] = dataset.uri
                record['result'] = result

                # some fields to return some rendering information for the frontend.
                try:
                    record['title'] = dataproduct[dataset.title_field]
                except:
                    pass

                try:
                    record['thumbnail'] = dataproduct[dataset.thumbnail_field]
                except:
                    pass

                try:
                    record['url'] = dataproduct[dataset.url_field]
                except:
                    pass

                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['result'] =  str(error)
            results.append(record)

        return results