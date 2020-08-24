"""
    File name: service_base.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP service abstract base class.
                  This shows what the services should implement.
"""

class query_base:

    # Initializer
    def __init__(self, url):
        self.url = url

    # implement this in the derived service classes
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        pass

    # implement this in the derived service classes
    def run_query(self, dataset, dataset_name, query, override_access_url=None, override_service_type=None):
        pass

    # implement this in the derived service classes
    def get_services(self, service_type, keyword):
        pass

    # implement this in the derived service classes
    def get_table_fields(self, dataset, access_url):
        pass

    def nico(self):
        pass