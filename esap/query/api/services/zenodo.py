"""
    File name: zenodo.py
    Date created: 2021-05-16
    Description:  Zenodo Service Connector for ESAP.
"""
#from eossr.api import get_ossr_records
from eossr.api import get_zenodo_records
from rest_framework import serializers
from .query_base import query_base
import requests
import json
import logging
import string

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = "_and_"

# The request header
#ZENODO_HOST = "https://zenodo.org/api/communities"
#ZENODO_AUTH_TOKEN = "REMOVED"

#URLPATTERNS = dict(
    #scope="{host}/scopes/",
    #dids="{host}/dids/{scope}/",
    #files="{host}/dids/{scope}/files/",
    #replicas="{host}/replicas/{scope}/"
#)

# --------------------------------------------------------------------------------------------------------------------


class zenodo_connector(query_base):
    """
    The connector to access the data lake through ZENODO
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for the ZENODO REST API
    def construct_query(
        self, dataset, esap_query_params, translation_parameters, equinox
    ):

        logger.info("AAAA" + str(esap_query_params))

        query = {'size': '1000'}
        where = {}
        error = {}


        logger.info("BBBB" + str(query))

        query['communities'] =  str.lower(esap_query_params.pop('community')[0])

        logger.info("CCCC" + str(query))

        if 'keyword' in esap_query_params.keys():
             query['keywords'] =  str(esap_query_params.pop('keyword')[0])

        desired_value = 'undefined'
        for key, value in query.items():
          if value == desired_value:
            del query[key]
            break

        logger.info("DDDDD" + str(query))

        return query, where, error

    def _get_data_from_zenodo(self, query, session):
        """ use Zenodo REST API to query the data lake """

        results = []
        response = []

        logger.info("OOOOOOO" + str(query))

        if query != "empty":
            try:
                 response = get_zenodo_records(**query)
            except:
                 logger.info("No Results Found 1")
        else:
             logger.info("empty!!")

        if len(response) > 0:
            results = [
                element.data
                for element in response
             ]

        return results

    def run_query(
        self,
        dataset,
        dataset_name,
        query,
	session,
        override_access_url=None,
        override_service_type=None,
    ):
        """
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;
        """

        # create a function that reads the data from lofar
        zenodo_results = self._get_data_from_zenodo(query, session)

        ##logger.info("RESULTS: " + str(zenodo_results))
        return zenodo_results

    # custom serializer for the 'query' endpoint

    class TypeToSerializerMap:

        map = {
            type(float): serializers.FloatField(),
            type(int): serializers.IntegerField(),
            type(str): serializers.CharField(),
            type(dict): serializers.DictField(),
            type(list): serializers.ListField(),
        }

        @classmethod
        def getFieldForType(cls, value):
            return cls.map.get(type(value), serializers.JSONField())

    class CreateAndRunQuerySerializer(serializers.Serializer):
        """
        Custom serializer classes implement dynamic field definition based on
        the contents of the query passed to it.
        """

        def __init__(self, *args, **kwargs):

            self.example_result = kwargs.get("instance", [])[0]

            super().__init__(*args, **kwargs)

            self.fields.update(
                {
                    key: zenodo_connector.TypeToSerializerMap.getFieldForType(value)
                    for key, value in self.example_result.items()
                }
            )
