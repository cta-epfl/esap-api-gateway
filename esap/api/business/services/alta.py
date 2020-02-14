"""
    File name: vo_services.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for ALTA.
"""

from .esap_service import esap_service

class observations_connector(esap_service):

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

        query = ''
        where = ''
        error = None

        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]
                where = where + dataset_key + '=' + value + '&'

            except Exception as error:
                # if the parameter could not be translated, then just continue
                error = "ERROR: translating key " + esap_key + ' ' + str(error)
                return query, error

        # cut off the last separation character
        where = where[:-1]

        # construct the query url
        query = self.url + '?' + where

        return query, error


    def run_query(self, dataset, query):
        # todo: implement ALTA query
        urls = []
        urls.append(query)
        return urls