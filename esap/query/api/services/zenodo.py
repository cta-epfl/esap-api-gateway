"""Zenodo Service Connector for ESAP."""

from eossr.api import get_zenodo_records
from rest_framework import serializers
from .query_base import query_base
import logging

logger = logging.getLogger(__name__)


class zenodo_connector(query_base):
    """A connector to query Zenodo archives"""

    # construct a query for the ZENODO REST API
    def construct_query(self, dataset, esap_query_params, translation_parameters):

        query = {"size": "1000"}
        where = {}
        error = {}

        query["communities"] = esap_query_params.pop("community")[0]

        if "keyword" in esap_query_params.keys():
            query["keywords"] = str(esap_query_params.pop("keyword")[0])

        desired_value = "undefined"
        for key, value in query.items():
            if value == desired_value:
                del query[key]
                break

        return query, where, error

    def _get_data_from_zenodo(self, query, session):
        """use Zenodo REST API to query the data lake"""

        results = []
        response = []

        if query != "empty":
            try:
                response = get_zenodo_records(**query)
            except:
                logger.info("No Results Found in Zenodo Archive Search")
        else:
            logger.info("Empty search in Zenodo Archive Search")

        if len(response) > 0:
            results = [element.data for element in response]

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

        zenodo_results = self._get_data_from_zenodo(query, session)
        logger.debug("RESULTS: " + str(zenodo_results))
        return zenodo_results

    class CreateAndRunQuerySerializer(serializers.Serializer):
        links = serializers.DictField()
        metadata = serializers.DictField()
        doi = serializers.CharField()
