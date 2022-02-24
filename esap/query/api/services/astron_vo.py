"""
    File name: vo.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for VO.
"""
from collections import namedtuple
from rest_framework import serializers
from .query_base import query_base
import pyvo as vo

SEPARATOR = ' AND '

def create_cone_search(esap_query_params, translation_parameters):
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
        cone_search = "CONTAINS(POINT('ICRS'," + \
                      translation_parameters['ra'] + "," + \
                      translation_parameters['dec'] + "), " \
                      "CIRCLE('ICRS'," + str(ra) + "," + str(dec) + "," + str(radius) + "))=1"

        # remove ra,dec,fov from the parameters so that they are not used in the where clause
        del esap_query_params['ra']
        del esap_query_params['dec']
        del esap_query_params['fov']
        return cone_search
    return ''


class tap_service_connector(query_base):

    # Initializer
    def __init__(self, url):
        self.url = url

        # cut off the '/sync' resource, because the vo.dal.TAPServices will add it again
        if self.url.endswith('/sync'):
            self.url = self.url[:-4]

    # construct a query for this type of service
    def construct_query(self, dataset, query_params, translation_parameters, override_resource=None):

        esap_query_params = dict(query_params)
        where = ''
        errors = []
        limit = "1000"

        # cone search is a specific type of query that uses ra, dec and a search radius.
        # it is also done with a specific ADQL syntax.
        # First check if the incoming query describes a cone search.

        cone_search = create_cone_search(esap_query_params,translation_parameters)

        for esap_param in esap_query_params:

            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            # handle 'keywords' and translate it to 'collection_id'
            try:
                # skip pagination parameters
                # they are not 'esap parameters', and not used in VO
                if not esap_key in ['page', 'page_size']:
                    dataset_key = translation_parameters[esap_key]
                    where = where + dataset_key + "='" + value + "'" + SEPARATOR

                if esap_key == 'page_size':
                    limit = value

            except Exception as error:
                # if the parameter could not be translated, use it raw and continue
                where = where + esap_key + "='" + value + "' " + SEPARATOR
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # add sync (or async) specifier
        query = self.url + '/sync'

        # add fixed ADQL parameters
        query = query + "?lang=ADQL&REQUEST=doQuery"

        # add query ADQL parameters (limit to 1000 results)
        query = query + "&QUERY=SELECT TOP " + limit + " * from "

        # if the parameter '&resource=...' is given to the url, then use that resource..
        if override_resource:
            query = query + override_resource
        else:
            # ... otherwise use the resource as defined in the datasets
            query = query + dataset.resource_name

        # add ADQL where clause
        if len(where)>0:
            query = query + " WHERE "
            query = query + where

        if len(cone_search)>0:
            if len(where) == 0:
                # if now previous where clause was added, then add the 'WHERE' keyword here
                query = query + " WHERE "

            query = query + cone_search

        # if query ends with a separation character then cut it off
        if query.endswith(SEPARATOR):
            query = query[:-len(SEPARATOR)]

        # the same for the 'where' clause
        if where.endswith(SEPARATOR):
            where = where[:-len(SEPARATOR)]
        return query, where, errors


    # run a query
    def run_query(self,
                  dataset, dataset_name, query, session=None, override_access_url=None, override_service_type=None):
        """
        # use pyvo to do a vo query
        :param dataset: the dataset object that must be queried
        :param query: the constructed (adql) query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with results from the query

        """

        results = []

        # use pyvo the get to the results
        service = vo.dal.TAPService(self.url)
        try:
            resultset = service.search(query)

        except Exception as error:
            return "ERROR: " + str(error)

        # if * then iterate on the full row, otherwise just on the selection
        if dataset.select_fields == "*":
            select_list = resultset.fieldnames
        else:
            select_list = dataset.select_fields.split(',')

        for row in resultset:
            # for the definition of standard fields to return see:
            # http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf

            record = {}

            result = ",".join(str(row[key]) for key in select_list)

            record['dataset'] = dataset.uri
            record['dataset_name'] = dataset_name
            record['result'] = result
            record['query'] = query

            # add some fields to return some rendering information for the frontend.
            # for ivoa.obscore field names see: http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf

            # We'll map field "src" in the result to field "dst" in the output
            # record. If "src" doesn't exist, we'll use "default" if specified,
            # otherwise we won't set the field.
            KeywordMapping = namedtuple('KeywordMapping', ['src', 'dst', 'default'])
            keyword_mappings = [
                KeywordMapping(dataset.title_field, 'title', None),
                KeywordMapping('dataproduct_type', 'dataproduct_type', None),
                KeywordMapping('calib_level', 'calibration_level', None),
                KeywordMapping('calib_level', 'level', None),
                KeywordMapping(dataset.thumbnail_field, 'thumbnail', ''),
                KeywordMapping(dataset.url_field, 'url', None),
                KeywordMapping('target_name', 'name', 'unknown'),
                KeywordMapping('target_name', 'target', None),
                KeywordMapping('s_ra', 'ra', None),
                KeywordMapping('s_dec', 'dec', None),
                KeywordMapping('s_fov', 'fov', None),
                KeywordMapping('s_fov', 'fov', None),
                KeywordMapping('obs_collection', 'obs_collection', None),
                KeywordMapping('obs_collection', 'collection', 'unknown'),
                KeywordMapping('access_estsize', 'size', None),
                KeywordMapping('facility_name', 'facility', None),
                KeywordMapping('instrument_name', 'instrument', None)
            ]
            for mapping in keyword_mappings:
                if mapping.src in row:
                    record[mapping.dst] = row[mapping.src]
                elif mapping.default is not None:
                    record[mapping.dst] = mapping.default

            results.append(record)

        return results


    # custom serializer for the 'query' endpoint
    class CreateAndRunQuerySerializer(serializers.Serializer):

        # required esap_fields
        name = serializers.CharField()
        collection = serializers.CharField()
        level = serializers.CharField()
        ra = serializers.FloatField()
        dec = serializers.FloatField()
        fov = serializers.FloatField()

        # extra fields
        dataset = serializers.CharField()
        result = serializers.CharField()

        dataproduct_type = serializers.CharField()
        calibration_level = serializers.IntegerField()
        target = serializers.CharField()
        obs_collection = serializers.CharField()
        size = serializers.IntegerField()
        facility = serializers.CharField()
        instrument = serializers.CharField()
        url = serializers.CharField()
        thumbnail = serializers.CharField()

        class Meta:
            fields = '__all__'
