from rest_framework import serializers
import requests
import json
import logging
import string
import urllib
from eossr.api import get_ossr_records

logger = logging.getLogger(__name__)

ZENODO_HOST = "https://zenodo.org/api/communities"
ZENODO_AUTH_TOKEN = "AUTH_TOKEN"



class Harvester(object):
    """
    The Harvester class used to collect entries for existing Worfklows / Notebooks from the OSSR
    """

    # Initializer
    def __init__(self, url = ZENODO_HOST):
        # We may end up using this when we switch to the sandbox version
        self.url = url

    @staticmethod
    def get_data_from_zenodo(query=None, keyword=None):
        """ use Zenodo REST API to query the OSSR"""

        def _format_results(records):
            results = []
            for record in records:

                try:
                    item = {}
                    codemeta =  record.get_codemeta()
                    item["id"] = record.data["id"]
                    item["description"] = record.data["metadata"].get("description","")
                    item["name"] = record.data["metadata"].get("title","")
                    item["workflow"] = "notebook"
                    item["url"] = codemeta.get("codeRepository","")
                    item["runtimePlatform"] = codemeta.get("runtimePlatform","")
                    item["keywords"] = ", ".join(codemeta.get("keywords",[]))
                    item["author"] = codemeta["author"][0].get("givenName","") + " " + codemeta["author"][0].get("familyName", "")
                    item["ref"] = "HEAD"
                    item["filepath"] = ""

                except Exception as e:
                    item = {}
                    logging.exception(e)
                finally:
                    results.append(item)
            return results

        keywords='jupyter-notebook'
        # Keep for later when we implement a keyword search: escape_records = get_ossr_records(search=query, keywords=keywords) if query else get_ossr_records(keywords=keywords)
        escape_records = get_ossr_records(keywords=keywords)
        return _format_results(escape_records)
