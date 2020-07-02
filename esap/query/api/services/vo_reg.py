"""
    File name: vo_reg.py
    Author: Nico Vermaas - Astron
    Date created: 2020-04-09
    Description:  ESAP services for VO registry
"""

from .query_base import query_base
import pyvo as vo
from pyvo.registry import search as regsearch
import urllib.parse

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


class vo_registry_connector(query_base):

    # Initializer
    def __init__(self, url):
        self.url = url

        # cut off the '/sync' resource, because the vo.dal.TAPServices will add it again
        if self.url.endswith('/sync'):
            self.url = self.url[:-4]


    # construct a query for this type of service
    def construct_query(self, dataset, query_params, translation_parameters, equinox):

        esap_query_params = dict(query_params)
        where = ''
        errors = []

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
                errors.append("ERROR: translating key " + esap_key + ' ' + str(error))


        results = []
        services = []

        if "keyword" in esap_query_params:
            services = self.search([esap_query_params["keyword"]])
        else :
            services = self.search(datamodel='ObsCore')

        for resource in services:
            # see row attributes
            # https://pyvo.readthedocs.io/en/latest/api/pyvo.registry.regtap.RegistryResource.html#pyvo.registry.regtap.RegistryResource
            #resource.describe()

            service = resource.service

            result = {}
            # ESAP attributes
            result['query_id'] = resource.ivoid
            result['dataset'] = dataset.uri
            result['dataset_name'] = resource.short_name
            result['output_format'] = str(resource.source_format)
            result['resource_name'] = str(dataset.resource_name)
            result['protocol'] = str(dataset.dataset_catalog.protocol)
            result['esap_service'] = str(dataset.dataset_catalog.esap_service)
            result['service_connector'] = str(dataset.service_connector)

            # VO RegistryResource attributes
            result['service_url'] = str(resource.access_url)
            result['access_url'] = str(resource.access_url)
            result['content_levels'] = str(resource.content_levels)
            result['content_types'] = str(resource.content_types)
            result['creators'] = str(resource.creators)
            result['ivoid'] = str(resource.ivoid)
            result['reference_url'] = str(resource.reference_url)
            result['region_of_regard'] = str(resource.region_of_regard)
            result['res_description'] = str(resource.res_description)
            result['res_title'] = str(resource.res_title)
            result['res_type'] = str(resource.res_type)
            result['short_name'] = resource.short_name
            result['source_format'] = str(resource.source_format)
            result['standard_id'] = str(resource.standard_id)
            result['waveband'] = ' '.join([str(elem) for elem in resource.waveband])
            #result['waveband'] = str(resource.waveband)

            # add sync (or async) specifier
            # query = resource.access_url + '/sync'

            query = resource.access_url + '/sync' if  (self.get_service_type(resource).upper() == "TAP") else resource.access_url
            # add fixed ADQL parameters
            query_params = {}
            query_params["LANG"] = "ADQL"
            query_params["REQUEST"] = "doQuery"
            query_params["QUERY"] = "SELECT TOP 10 * from " + dataset.resource_name


            # add ADQL where where
            if where:
                if len(where)>0:
                    # cut off the last separation character

                    query_params["QUERY"] += " WHERE " + where

            if cone_search:
                if len(cone_search)>0:
                    if len(where)>0:
                        query_params["QUERY"] += " AND " + cone_search
                    else:
                        query_params["QUERY"] += " WHERE " + cone_search

            result['query'] = query  + "?" + urllib.parse.urlencode(query_params)


            results.append(result)

        return results, errors


    # run a query
    def run_query(self, dataset, dataset_name, query):
        """
        # use pyvo to do a vo query
        :param dataset: the dataset object that must be queried
        :param query: the constructed (adql) query (that was probably generated with the above construct_query function)
        """

        results = []

        # use pyvo the get to the results

        service = vo.dal.TAPService(self.url)
        try:
            resultset = service.search(query)
        except Exception as error:
            record = {}
            record['query'] = query
            record['dataset'] = dataset.uri
            record['dataset_name'] = dataset_name
            record['result'] =  str(error)
            results.append(record)
            return results

        for row in resultset:
            # for the definition of standard fields to return see:
            # http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf

            record = {}
            result = ''

            # if * then iterate on the full row, otherwise just on the selection
            if dataset.select_fields=='*':
                values = row.values()

                for value in values:
                    try:
                        result = result + value.decode('utf-8') + ','
                    except:
                        try:
                            result = result + str(value) + ','
                        except:
                            pass
            else:
                select_list = dataset.select_fields.split(',')

                for select in select_list:
                    result = result + row[select].decode('utf-8') + ','

            # cut off the last ','
            result = result[:-1]
            record['dataset'] = dataset.uri
            record['dataset_name'] = dataset_name
            record['result'] = result
            record['query'] = query

            # add some fields to return some rendering information for the frontend.
            # for ivoa.obscore field names see: http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf
            try:
                record['title'] = row[dataset.title_field]
            except:
                pass

            try:
                record['thumbnail'] = row[dataset.thumbnail_field]
            except:
                pass

            try:
                record['url'] = row[dataset.url_field]
            except:
                pass


            results.append(record)

        return results


    # Search for a keyword
    def search(self, keywords=None, servicetype="tap", datamodel=None, waveband=None, **kwargs):
        """
        # Use pyvo to do a Registry search by keyword
        :param keyword: The keyword to search for
        :param servicetype: The service type that we are searching for (e.g. tap)
        """

        if datamodel:
            services = regsearch(datamodel=datamodel)
        else:
            services = regsearch(keywords=keywords, servicetype=servicetype, waveband=waveband) if waveband  else regsearch(keywords=keywords, servicetype=servicetype)

        return services



    def get_service_type (self, service):
        """
        # Get the IVOA Service Type
        :param service: The service ->  pyvo.registry.regtap.RegistryResource
        """
        servicetype = None

        standards = {
            "ivo://ivoa.net/std/tap" : "TAP",
            "ivo://ivoa.net/std/sia" : "SIA",
            "ivo://ivoa.net/std/obscore" : "OBSCORE",
            }

        if not service:
            return servicetype

        return standards[service["standard_id"].decode('utf-8').lower()] if service["standard_id"] else None

