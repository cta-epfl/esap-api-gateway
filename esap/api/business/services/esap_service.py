"""
    File name: vo_services.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP service base class
"""

class esap_service:

    # Initializer
    def __init__(self, url):
        self.url = url

    # implement this in the derived service classes
    def construct_query(self, table_name, esap_query_params, translation_parameters):
        pass

    # implement this in the derived service classes
    def run_query(self, query):
        pass