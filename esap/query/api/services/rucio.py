"""
    File name: rucio.py
    Date created: 2020-10-15
    Description:  Rucio Service Connector for ESAP.
"""

from rest_framework import serializers
from .query_base import query_base
import requests
import json
import logging

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = '_and_'

# The request header
RUCIO_HOST = "https://escape-rucio.cern.ch:32300"

# --------------------------------------------------------------------------------------------------------------------


def get_data_from_rucio(query):
    """ use Rucio REST API to query the data lake """

    # authenticate user using X509 certificates
    # curl --insecure -i --cert ~/.globus/client.crt -i --key ~/.globus/client.key -i -H "X-Rucio-Account: meyer" -X GET "https://escape-rucio.cern.ch:32301/auth/x509"

    # export RUCIO_AUTH_TOKEN="meyer-/DC=org/DC=terena/DC=tcs/C=NL/O=ASTRON/CN=meyer 1775@astron.nl-unknown-*"
    # validate user
    # curl --insecure -X GET -H "X-Rucio-Auth-Token: $RUCIO_AUTH_TOKEN" https://escape-rucio.cern.ch:32301/auth/validate

    # query DIDs with scope-name LOFAR_ASTRON_GRANGE
    # curl --insecure -X GET -H "X-Rucio-Auth-Token: $RUCIO_AUTH_TOKEN" https://escape-rucio.cern.ch:32300/dids/LOFAR_ASTRON_GRANGE/

    # list of scope names
    # ESCAPE_CERN_TEAM-noise
    # CMS_INFN_DCIANGOT
    # SKA_SKAO_COLLINSON
    # ESCAPE_DESY_TEAM-testing
    # FAIR_GSI_SZUBA
    # SKA_SKAO_JOSHI-testing
    # CTA_LAPP_FREDERIC
    # SKA_SKAO_BARNSLEY-testing
    # ESCAPE_CERN_TEAM
    # VIRGO_EGO_CHANIAL
    # ESCAPE_CERN_TEAM-testing
    # LSST_CCIN2P3_GOUNON
    # ATLAS_LAPP_JEZEQUEL
    # SKA_SKAO_COLL-testing
    # MAGIC_PIC_BRUZZESE
    # LOFAR_ASTRON_GRANGE
    logger.info(results)

    return list(results)


class rucio_connector(query_base):
    """
    The connector to access the data lake through RUCIO
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service

    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

        where = ''
        errors = []

        # translate the esap_parameters to specific catalog parameters
        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translateget_data_from_lofard not translating key " +
                            esap_key + ' ' + str(error)+', using it raw.')
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # if query ends with a separation character then cut it off
        if where.endswith(AMP_REPLACEMENT):
            where=where[:-len(AMP_REPLACEMENT)]

        # Zheng, this is where you could change the format of the Rucio query.
        # this is not required, you can also leave it like this.
        # The 'query' variable that is returned is already translated with the Rucio parameter_mapping
        # here. I only used some example paramters, so you may still want to change the parameter_mapping.

        # construct the query url
        # for now simply like: 'https://escape-rucio.cern.ch:32300/dids/LOFAR_ASTRON_GRANGE/'
        query=self.url + '?' + where
        logger.info('construct_query: '+query)
        return query, where, errors

    def run_query(self, dataset, dataset_name, query, override_access_url = None, override_service_type = None):
        """
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;
        """
        logger.info('query:'+query)
        results=[]

        # create a function that reads the data from lofar
        # rucio_results = get_data_from_rucio(query)

        try:
            for rucio_result in rucio_results:
                record={}
                record['name']=rucio_result['name']
                record['parent']=rucio_result['parent']
                record['level']=rucio_result['level']
                record['bytes']=rucio_result['bytes']
                record['scope']=rucio_result['scope']
                record['type']=rucio_result['type']

                results.append(record)

        except Exception as error:
            return "ERROR: " + str(error)

        return results

    # custom serializer for the 'query' endpoint

    class CreateAndRunQuerySerializer(serializers.Serializer):

        # Zheng: this defines the structure of the response to /esap/query/query for Rucio
        # the fields should be the same as in run-query

        name=serializers.CharField()
        parent=serializers.CharField()
        level=serializers.IntegerField()
        size_in_bytes=serializers.IntegerField()
        scope=serializers.CharField()
        result_type=serializers.CharField()

        class Meta:
            fields='__all__'
