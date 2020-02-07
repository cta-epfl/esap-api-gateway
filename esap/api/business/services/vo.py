"""
    File name: vo_services.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for VO.
"""

from .esap_service import esap_service
import pyvo as vo


def create_cone_search(esap_query_params, translation_parameters, equinox):
    """
    Return a cone search subquery when ra, dec and fov are found in the query parameters.

    example:
    SELECT TOP 10 * from ivoa.obscore WHERE CONTAINS(POINT('ICRS',s_ra,s_dec), CIRCLE('ICRS',202.48,47.23,4.0))=1

    :param esap_query_params:
    :param translation_parameters:
    :return:
    """

    radius = None
    try:
        ra = float(esap_query_params['ra'][0])
        dec = float(esap_query_params['dec'][0])
        radius = float(esap_query_params['fov'][0])
    except:
        pass

    if radius != None:
        # found a fov parameter, which indicates a cone search
        cone_search = "CONTAINS(POINT('"+equinox+"'," + \
                      translation_parameters['ra'] + "," + \
                      translation_parameters['dec'] + "), " \
                      "CIRCLE('"+equinox+"'," + str(ra) + "," + str(dec) + "," + str(radius) + "))=1"

        # remove ra,dec,fov from the parameters so that they are not used in the where clause
        del esap_query_params['ra']
        del esap_query_params['dec']
        del esap_query_params['fov']
        return cone_search


class tap_service(esap_service):

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, table_name, query_params, translation_parameters, equinox):

        esap_query_params = dict(query_params)
        query = ''
        where = ''
        error = None

        # cone search is a specific type of query that uses ra, dec and a search radius.
        # it is also done with a specific ADQL syntax.
        # First check if the incoming query describes a cone search.

        cone_search = create_cone_search(esap_query_params,translation_parameters, equinox)

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


        # add sync (or async) specifier
        query = self.url + '/sync' \
            # query = url

        # add fixed ADQL parameters
        query = query + "?lang=ADQL&REQUEST=doQuery"

        # add query ADQL parameters (limit to 10 results)
        query = query + "&QUERY=SELECT TOP 10 * from " + table_name

        # add ADQL where where
        query = query +" WHERE "
        if len(where)>0:
            # cut off the last separation character
            where = where[:-1]
            query = query + where

        if len(cone_search)>0:
            query = query + cone_search

        return query, error

    # run a query
    def run_query(self, query):
        """
        # use pyvo to do a vo query
        :param url: acces url of the vo service
        :param query: adql query
        :return:
        """

        access_url=None
        urls = []

        # use pyvo the get to the results
        service = vo.dal.TAPService(self.url)
        resultset = service.search(query)

        for row in resultset:
            # for the definition of standard fields to return see:
            # http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf

            # todo: read 'access_url' from catalog parameters also
            access_url = row["access_url"].decode('utf-8')
            urls.append(access_url)
            print(access_url)

        return urls