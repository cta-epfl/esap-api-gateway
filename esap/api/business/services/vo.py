"""
    File name: vo_services.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for VO.
"""

from .esap_service import esap_service
import pyvo as vo

class tap_service(esap_service):

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, table_name, esap_query_params, translation_parameters):

        query = ''
        where = ''
        error = None

        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]
                where = where + dataset_key + "='" + value + "' "

            except Exception as error:
                # if the parameter could not be translated, then just continue
                error = "ERROR: translating key " + esap_key + ' ' + str(error)
                return query, error

        # cut off the last separation character
        where = where[:-1]

        # construct the call
        # example:
        # https://vo.astron.nl/__system__/tap/run/tap/sync/?lang=ADQL&REQUEST=doQuery&QUERY=SELECT TOP 10 * from ivoa.ObsCore

        # add sync (or async) specifier
        query = self.url + '/sync' \
            # query = url

        # add fixed ADQL parameters
        query = query + "?lang=ADQL&REQUEST=doQuery"

        # add query ADQL parameters (limit to 10 results)
        query = query + "&QUERY=SELECT TOP 10 * from " + table_name

        # add ADQL where where
        query = query + " where " + where

        return query, error

    # run a query
    def run_query(self, query):
        """
        # use pyvo to do a vo query
        :param url: acces url of the vo service
        :param query: adql query
        :return:
        """

        obs_title=None
        access_url=None

        # use pyvo the get to the results
        service = vo.dal.TAPService(self.url)
        resultset = service.search(query)

        for row in resultset:
            # for the definition of standard fields to return see:
            # http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf
            obs_title = row["obs_title"].decode('utf-8')
            access_url = row["access_url"].decode('utf-8')

        print(obs_title,access_url)
        return access_url