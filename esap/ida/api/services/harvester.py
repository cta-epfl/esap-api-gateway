import concurrent.futures
import logging

from eossr.api import get_ossr_records

logger = logging.getLogger(__name__)

ZENODO_HOST = "https://zenodo.org/api/communities"
ZENODO_AUTH_TOKEN = "AUTH_TOKEN"


class Harvester(object):
    """
    The Harvester class used to collect entries for existing Worfklows / Notebooks from the OSSR
    """

    # Initializer
    def __init__(self, url=ZENODO_HOST):
        # We may end up using this when we switch to the sandbox version
        self.url = url

    @staticmethod
    def get_data_from_zenodo(query=None, keyword=None, timeout=5.0):
        """Use the Zenodo REST API to query the OSSR

        Parameters
        ----------
        query : `str`
            Unused.
        keyword : `str`
            Unused.
        timeout : `float`
            Give up if Zenodo doesn't return within timeout seconds.

        Notes
        -----
        This method uses a thread pool to submit multiple queries to Zenodo at
        once, and has a timeout on each one. This prevents it from blocking
        indefinitely (or even for num_records * timeout seconds) if Zenodo is
        unresponsive.
        """

        def _format_results(records):
            results = []

            def item_from_record(record, timeout):
                item = {}
                try:
                    codemeta = record.get_codemeta(timeout=timeout)
                    item["id"] = record.data["id"]
                    item["description"] = record.data["metadata"].get("description", "")
                    item["name"] = record.data["metadata"].get("title", "")
                    item["workflow"] = "notebook"
                    item["url"] = codemeta.get("codeRepository", "")
                    item["runtimePlatform"] = codemeta.get("runtimePlatform", "")
                    item["keywords"] = ", ".join(codemeta.get("keywords", []) + ['ossr'])
                    item["author"] = ", ".join(
                        [
                            " ".join(
                                author.get(fieldName, "")
                                for fieldName in ("givenName", "familyName")
                            ).strip()
                            for author in codemeta.get("author", [])
                        ]
                    )
                    item["ref"] = "HEAD"
                    item["filepath"] = ""
                except Exception as e:
                    logging.exception(e)
                return item

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(item_from_record, record, timeout)
                    for record in records
                ]
                for future in concurrent.futures.as_completed(futures):
                    item = future.result()
                    if "url" in item and item["url"]:
                        results.append(item)

            return results

        keywords = "jupyter-notebook"
        # keywords = "GRB"
        # Keep for later when we implement a keyword search:
        # escape_records = (
        #     get_ossr_records(search=query, keywords=keywords)
        #     if query
        #     else get_ossr_records(keywords=keywords)
        # )
        escape_records = get_ossr_records(keywords=keywords)
        return _format_results(escape_records)
