"""
    File name: alta.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for ALTA.
"""

from .query_base import query_base
import requests, json
import logging

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = '_and_'

# The request header
ALTA_HOST = "https://alta.astron.nl/altapi"
ALTA_WEBDAV_HOST = "https://alta.astron.nl/webdav/"
ALTA_HEADER = {
    'content-type': "application/json",
}

# --------------------------------------------------------------------------------------------------------------------

class alta_connector(query_base):
    """
    The connector to access the ALTA dataproducts dataset
    """

    # Initializer
    def __init__(self, url):
        self.url = url


    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

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

        # make a selection of dataproductSubTypes
        # based on the defined 'collection' and 'level' of this dataset.

        if where != '':
            where = where + AMP_REPLACEMENT

        if 'IMAGING' in dataset.collection.upper():
            # instrument__icontains=APERTIF
            if 'RAW' in dataset.level.upper():
                where = where + "dataProductSubType__in=uncalibratedVisibility"

            if 'PROCESSED' in dataset.level.upper():

                # these are not observations, but pipelines. Access activities
                self.url = self.url.replace('observations','activities')
                where = where + "dataProductSubType__in=calibratedVisibility,continuumMF,continuumChunk,imageCube,beamCube,polarisationImage,polarisationCube,continuumCube"

        if 'TIMEDOMAIN' in dataset.collection.upper():
            where = where + "project__externalRef=ARTSSC"
            where = where + "dataProductSubType=pulsarTimingTimeSeries"
            # instrument__icontains=ARTS
            # http://localhost/altapi/activities?project__externalRef=ARTSSC

        # if query ends with a separation character then cut it off
        if where.endswith(AMP_REPLACEMENT):
            where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url
        query = self.url + '?' + where
        return query, where, errors


    def run_query(self, dataset, dataset_name, query):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;

         example:
        /esap-api/run-query/?dataset_uri=apertif-imaging-rawdata&query=https://alta.astron.nl/altapi/observations-flat?view_ra=342.16_and_view_dec=33.94_and_view_fov=10_and_dataProductType=image_and_dataProductSubType=continuumMF

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

            logger.info('observations in response: '+str(len(observations)))

            # iterate over the list of results.. and gather the runid's in a comma separated list for the next query on datasetid
            list = []
            for observation in observations:
                list.append(observation['runId'])

            runids = ','.join(list)

            # construct a second query on dataproducts for the gathered runId's
            host = ALTA_HOST
            if "/observations" in query:
                query_list = query.split('/observations')
                host = query_list[0]

            elif "/activities" in query:
                query_list = query.split('/activities')
                host = query_list[0]


            # there may be additional query parameters in the original query, like dataProductSubType=continuumMF
            # copy them over to the secondary query as well.
            filter = '&' + query_list[1].split('?')[1]
            dataproduct_query = host + '/dataproducts-flat?datasetID__in=' + str(runids) + filter

            # shortcut to add an extra selection criterium... handle better later
            # dataproduct_query = dataproduct_query + "&dataProductSubType=continuumMF"

            # execute the secondary query to dataproducts
            response = requests.request("GET", dataproduct_query, headers=ALTA_HEADER)

            json_response = json.loads(response.text)
            dataproducts = json_response["results"]


            for dataproduct in dataproducts:

                record = {}
                result = ''

                record['name'] = dataproduct['name']
                record['PID'] = dataproduct['PID']
                record['dataProductType'] = dataproduct['dataProductType']
                record['dataProductSubType'] = dataproduct['dataProductSubType']

                # result = "https://alta.astron.nl/science/details/"+observation["runId"]
                record['generatedByActivity'] = dataproduct['generatedByActivity'][0]
                record['datasetID'] = dataproduct['datasetID']
                # record['target'] = "???"
                record['RA'] = dataproduct['RA']
                record['dec'] = dataproduct['dec']
                record['fov'] = dataproduct['fov']


                # only send back thumbnails that are not placeholders.
                if record['dataProductSubType']=='continuumMF':
                    record['thumbnail'] = dataproduct['thumbnail']

                record['storageRef'] = dataproduct['storageRef']
                # construct the url based on the storageRef
                record['url'] = ALTA_WEBDAV_HOST + dataproduct['derived_release_id'] + '/' + dataproduct['storageRef']

                results.append(record)

        except Exception as error:
            record = {}
            record['query'] = query
            record['dataset'] = dataset.uri
            record['error'] =  str(error)
            results.append(record)

        return results
