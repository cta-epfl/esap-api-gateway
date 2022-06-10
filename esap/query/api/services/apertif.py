"""
    File name: alta.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP service connector for Apertif (ALTA).
"""
import urllib.parse as urlparse
from django.conf import settings
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
        try:
            if settings.USE_DOP457:
                url = "http://dop457.astron.nl/altapi"
        except:
            self.url = url + '/dataproducts'

    # create a paginated response.
    def get_paginated_response(self, results, query, json_response):
        record = {}

        # retrieve the requested page from the query
        try:
            page = int(urlparse.parse_qs(query)['page'][0])
        except:
            page = 1

        record['description'] = "ESAP API Gateway - ALTA"
        record['version'] = settings.API_VERSION,
        record['count'] = int(json_response["count"])
        record['requested_page'] = page
        record['pages'] = int(json_response["pages"])
        record['results'] = results
        return record

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters):
        where = ''
        errors = []

        # translate the esap_parameters to specific catalog parameters
        for esap_param in esap_query_params:
            value = esap_query_params[esap_param][0]

            try:
                dataset_key = translation_parameters[esap_param]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, set the where to an Error state
                if esap_param == "page_size" or esap_param == "page":
                    logger.info('pagination parameters added to the query; handled by the query_controller')
                    where = where + esap_param + '=' + value + AMP_REPLACEMENT
                else:
                    where = "Error: could not translate key " + esap_param + ' ' + str(error)

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

        # if no page_size is given, then set it here for ALTA, because ALTA default uses 500
        if not "page_size" in where:
            where = where + AMP_REPLACEMENT + "page_size=50"

        # if query ends with a separation character then cut it off
        if where.endswith(AMP_REPLACEMENT):
            where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url
        query = self.url + '?' + where
        if "Error" in where:
            query = 'empty'
            errors = [where]
            where = ''

        logger.info('construct_query: ' + query + "\nErrors: " + str(errors))
        return query, where, errors

    def run_query(self, dataset, dataset_name, query, session=None,
                  override_access_url=None, override_service_type=None):
        """
        # use the ALTA REST API to do a query
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: a paginated response containing the results of the requested page

         example:
        /esap-api/query/run-query/?dataset_uri=apertif-imaging-processeddata
        &query='https://alta.astron.nl/altapi/dataproducts?view_ra=342.16_and_view_dec=33.94_and_view_fov=10_and_dataProductSubType__in=calibratedVisibility,continuumMF,continuumChunk,imageCube,beamCube,polarisationImage,polarisationCube,continuumCube
        """

        def construct_vo_thumbnail(dataproduct):
            vo_host = "https://vo.astron.nl/getproduct/"

            # extract the path from storageref
            # 'cold:190809042_AP_B034/HI_image_cube1.fits => 190809042_AP_B034/HI_image_cube1.fits
            name = dataproduct['name']
            storageRef = dataproduct['storageRef']
            pos = storageRef.find(name)
            path = storageRef[0:pos - 1]

            # if there is a , or : still in a prefix, then remove all that
            pos = path.find(':') + 1
            if pos > 0:
                path = path[pos:]

            # if there is a , or : still in a prefix, then remove all that
            pos = path.find(',') + 1
            if pos > 0:
                path = path[pos:]

            postfix = "?preview=True&width=null"
            vo_url = vo_host + dataproduct['derived_release_id'] + '/' + path + '/' + name + postfix

            # stupid hack to overcome the difference between release_id and the path used in VO
            vo_url = vo_url.replace('APERTIF_DR1_Imaging', 'APERTIF_DR1')
            return vo_url

        def get_collection(dataProductSubType):

            collection = 'unknown'
            level = 'unknown'

            if dataProductSubType == 'uncalibratedVisibility':
                collection = 'imaging'
                level = '0'

            if dataProductSubType in 'calibratedVisibility':
                collection = 'imaging'
                level = '1'

            if dataProductSubType in 'continuumMF,continuumChunk,imageCube,beamCube,polarisationImage,polarisationCube,continuumCube':
                collection = 'imaging'
                level = '2'

            if dataProductSubType == 'pulsarTimingTimeSeries':
                collection = 'TIMEDOMAIN'
                level = '0'

            return collection, level

        results = []
        pagination_record = {}
        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT, '&')
        try:

            # execute the http request to ALTA and retrieve the dataproducts
            logger.info('run-query: ' + query)
            response = requests.request("GET", query, headers=ALTA_HEADER)

            json_response = json.loads(response.text)

            try:
                dataproducts = json_response["results"]
            except:
                raise Exception(json_response)

            # if a dataset is specified but the response is the same as for all results,
            # it means the dataset is not present in the db therefore the results should be none
            # example:
            #   https://alta.astron.nl/altapi/dataproducts?a=b
            #   gives back all records instead of none
            # Note: it is compared by the 'count' which is not very beautiful
            if dataset and json_response['count'] >= 300012:
                dataproducts = []

            for dataproduct in dataproducts:
                collection, level = get_collection(dataproduct['dataProductSubType'])
                record = {}
                record['dataset'] = dataset_name
                record['collection'] = collection
                record['level'] = level
                record['level'] = dataproduct['calibrationLevel']
                record['name'] = dataproduct['name']
                record['PID'] = dataproduct['PID']
                record['dataProductType'] = dataproduct['dataProductType']
                record['dataProductSubType'] = dataproduct['dataProductSubType']

                record['generatedByActivity'] = dataproduct['generatedByActivity'][0]
                record['datasetID'] = dataproduct['datasetID']
                # record['target'] = "???"
                record['ra'] = dataproduct['RA']
                record['dec'] = dataproduct['dec']
                record['fov'] = dataproduct['fov']
                record['release'] = dataproduct['derived_release_id']

                #                if record['dataProductSubType']=='continuumMF':
                #                    record['thumbnail'] = dataproduct['thumbnail']

                #                # add thumbnails for Apertif DR1
                #                if record['release']=='APERTIF_DR1_Imaging':
                #                    if (record['dataProductSubType']=='imageCube') or \
                #                            (record['dataProductSubType'] == 'continuumMF') or \
                #                            (record['dataProductSubType']=='polarisationImage') or \
                #                            (record['dataProductSubType']=='polarisationCube') :
                #                        record['thumbnail'] = construct_vo_thumbnail(dataproduct)

                # only send back thumbnails that are not static placeholders.
                if not 'static' in dataproduct['thumbnail']:
                    record['thumbnail'] = dataproduct['thumbnail']
                record['storageRef'] = dataproduct['storageRef']

                # construct the url to the data based on the storageRef
                record['url'] = ALTA_WEBDAV_HOST + dataproduct['derived_release_id'] + '/' + dataproduct['storageRef']

                results.append(record)

        except Exception as error:
            return "ERROR: " + str(error)

        # create a paginated response based on information from the query and the response
        paginated_results = self.get_paginated_response(results, query, json_response)

        return paginated_results
        # return results # unpaginated response

    # custom serializer for the 'query' endpoint
    class CreateAndRunQuerySerializer(serializers.Serializer):
        # required esap fields
        name = serializers.CharField()
        collection = serializers.CharField()
        fov = serializers.FloatField()
        ra = serializers.FloatField()
        dec = serializers.FloatField()
        url = serializers.CharField()

        # extra fields
        PID = serializers.CharField()
        dataProductType = serializers.CharField()
        dataProductSubType = serializers.CharField()
        generatedByActivity = serializers.CharField()
        datasetID = serializers.CharField()
        storageRef = serializers.CharField()

        class Meta:
            fields = '__all__'
