"""
    File name: alta.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for ALTA.
"""

from rest_framework import serializers
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
        self.url = url + '/dataproducts'


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
                # if the parameter could not be translated, use it raw and continue
                where = where + esap_key + "=" + value + AMP_REPLACEMENT
                logger.info("ERROR: could not translating key " + esap_key + ' ' + str(error)+', using it raw.')
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # cut off the last separation character
        where = where[:-len(AMP_REPLACEMENT)]

        # make a selection of dataproductSubTypes
        # based on the defined 'collection' and 'level' of this dataset.

        if where != '':
            where = where + AMP_REPLACEMENT

        if 'IMAGING' in dataset.collection.upper():

            if 'RAW' in dataset.level.upper():
                where = where + "dataProductSubType__in=uncalibratedVisibility"

            if 'PROCESSED' in dataset.level.upper():
                where = where + "dataProductSubType__in=calibratedVisibility,continuumMF,continuumChunk,imageCube,beamCube,polarisationImage,polarisationCube,continuumCube"

        if 'TIMEDOMAIN' in dataset.collection.upper():
              where = where + "dataProductSubType=pulsarTimingTimeSeries"

        # if query ends with a separation character then cut it off
        if where.endswith(AMP_REPLACEMENT):
            where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url
        query = self.url + '?' + where
        logger.info('construct_query: '+query)
        return query, where, errors


    def run_query(self, dataset, dataset_name, query, override_access_url=None, override_service_type=None):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;

         example:
        /esap-api/query/run-query/?dataset_uri=apertif-imaging-processeddata
        &query='https://alta.astron.nl/altapi/dataproducts?view_ra=342.16_and_view_dec=33.94_and_view_fov=10_and_dataProductSubType__in=calibratedVisibility,continuumMF,continuumChunk,imageCube,beamCube,polarisationImage,polarisationCube,continuumCube
        """

        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        try:

            # execute the http request to ALTA and retrieve the dataproducts
            logger.info('run-query: '+query)
            response = requests.request("GET", query, headers=ALTA_HEADER)

            json_response = json.loads(response.text)
            dataproducts = json_response["results"]

            logger.info('nr of dataproducts in response: '+str(len(dataproducts)))

            for dataproduct in dataproducts:

                record = {}
                result = ''

                record['name'] = dataproduct['name']
                record['PID'] = dataproduct['PID']
                record['dataProductType'] = dataproduct['dataProductType']
                record['dataProductSubType'] = dataproduct['dataProductSubType']

                record['generatedByActivity'] = dataproduct['generatedByActivity'][0]
                record['datasetID'] = dataproduct['datasetID']
                # record['target'] = "???"
                record['RA'] = dataproduct['RA']
                record['dec'] = dataproduct['dec']
                record['fov'] = dataproduct['fov']
                record['release'] = dataproduct['derived_release_id']

                # only send back thumbnails that are not static placeholders.
                if record['dataProductSubType']=='continuumMF':
                    record['thumbnail'] = dataproduct['thumbnail']

                record['storageRef'] = dataproduct['storageRef']

                # construct the url to the data based on the storageRef
                record['url'] = ALTA_WEBDAV_HOST + dataproduct['derived_release_id'] + '/' + dataproduct['storageRef']

                results.append(record)

        except Exception as error:
            record = {}
            record['query'] = query
            record['dataset'] = dataset.uri
            record['error'] =  str(error)
            results.append(record)

        return results


    # custom serializer for the 'query' endpoint
    class CreateAndRunQuerySerializer(serializers.Serializer):
        name = serializers.CharField()
        PID = serializers.CharField()
        dataProductType = serializers.CharField()
        dataProductSubType = serializers.CharField()
        generatedByActivity = serializers.CharField()
        datasetID = serializers.CharField()
        RA = serializers.FloatField()
        dec = serializers.FloatField()
        fov = serializers.FloatField()
        storageRef = serializers.CharField()
        url = serializers.CharField()

        class Meta:
            fields = '__all__'
