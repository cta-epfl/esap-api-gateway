"""
    File name: zenodo.py
    Date created: 2021-05-16
    Description:  Zenodo Service Connector for ESAP.
"""

from rest_framework import serializers
from .query_base import query_base
import requests
import json
import logging
import string

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = "_and_"

# The request header
ZENODO_HOST = "https://zenodo.org/api/communities"
ZENODO_AUTH_TOKEN = "REMOVED"

URLPATTERNS = dict(
    scope="{host}/scopes/",
    dids="{host}/dids/{scope}/",
    files="{host}/dids/{scope}/files/",
    replicas="{host}/replicas/{scope}/"
)

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

        query = {}
        where = {}
        errors = []

        query = dict(
            resource_category=esap_query_params.pop("resource_category", ["dids"])[0]
        )

        url_pattern = URLPATTERNS.get(
            query["resource_category"], URLPATTERNS.get("escape2020")
        )

        url_pattern_fields = [
            field[1] for field in string.Formatter().parse(url_pattern)
        ]

        try:
            url_params = {
                field: esap_query_params.pop(field, "Missing")[0]
                for field in url_pattern_fields
                if field is not None and field != "host"
            }

            # translate the remianing esap_parameters to specific catalog parameters
            where = {
                translation_parameters.get(key, key): value[0]
                for key, value in esap_query_params.items()
                if key not in ["catalog"]
            }
            query = dict(
                query_info=dict(
                    url_pattern=url_pattern, url_params=url_params, where=where
                )
            )
        except Exception as e:
            errors.append(f"Zenodo Connector {type(e)} {e}")

        return query, where, errors

    def _get_data_from_zenodo(self, query, session):
        """ use Zenodo REST API to query the data lake """
        #query_info = query["query_info"]
        #url = query_info["url_pattern"].format(
            #host=f"{self.url}", **query_info["url_params"]
        #)
        results = []
        response = requests.get(
             'https://zenodo.org/api/records',
                        params={'communities': 'escape2020',
                                'access_token': ZENODO_AUTH_TOKEN,
				'size': 100 }
       ) 
        if len(response.content.strip()):
            results = [
                json.loads(element)
               for element in response.content.decode("utf-8").strip().split("\n")
            ]


        ##logger.info("WHAT" + str(results))

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
        logger.info("query:" + str(query))

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
