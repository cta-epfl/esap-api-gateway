"""
    File name: esap_service.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP service abstract base class.
                  This shows what the services should implement.
"""

class esap_service:

    # Initializer
    def __init__(self, url):
        self.url = url

    # implement this in the derived service classes
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        pass

    # implement this in the derived service classes
    def run_query(self, dataset, query):
        pass