"""
    File name: vo.py
    Author: Nico Vermaas - Astron
    Date created: 2020-02-07
    Description:  ESAP services for VO.
"""
from rest_framework import serializers
from .query_base import query_base
import pyvo as vo

SEPARATOR = ' AND '

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
    return ''


class tap_service_connector(query_base):

    # Initializer
    def __init__(self, url):
        self.url = url

        # cut off the '/sync' resource, because the vo.dal.TAPServices will add it again
        if self.url.endswith('/sync'):
            self.url = self.url[:-4]

    # construct a query for this type of service
    def construct_query(self, dataset, query_params, translation_parameters, equinox, override_resource=None):

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

            # handle 'keywords' and translate it to 'collection_id'
            try:
                # skip pagination parameters
                # they are not 'esap parameters', and not used in VO
                if not esap_key in ['page', 'page_size']:
                    dataset_key = translation_parameters[esap_key]
                    where = where + dataset_key + "='" + value + "'" + SEPARATOR

            except Exception as error:
                # if the parameter could not be translated, use it raw and continue
                where = where + esap_key + "='" + value + "' " + SEPARATOR
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # add sync (or async) specifier
        query = self.url + '/sync'

        # add fixed ADQL parameters
        query = query + "?lang=ADQL&REQUEST=doQuery"

        # add query ADQL parameters (limit to 10 results)
        query = query + "&QUERY=SELECT * from "

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
    def run_query(self, dataset, dataset_name, query, override_access_url=None, override_service_type=None):
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
                record['title'] = row[dataset.title_field].decode('utf-8')
            except:
                pass

            try:
                record['dataproduct_type'] = row['dataproduct_type'].decode('utf-8')
            except:
                pass

            try:
                record['calibration_level'] = row['calib_level']
            except:
                pass

            try:
                record['thumbnail'] = row[dataset.thumbnail_field].decode('utf-8')
            except:
                pass

            try:
                record['url'] = row[dataset.url_field].decode('utf-8')
            except:
                pass

            try:
                record['ra'] = row['s_ra']
            except:
                pass

            try:
                record['dec'] = row['s_dec']
            except:
                pass

            try:
                record['fov'] = row['s_fov']
            except:
                pass

            try:
                record['target'] = row['target_name'].decode('utf-8')
            except:
                pass

            try:
                record['obs_collection'] = row['obs_collection'].decode('utf-8')
            except:
                pass

            try:
                record['size'] = row['access_estsize']
            except:
                pass

            try:
                record['facility'] = row['facility_name'].decode('utf-8')
            except:
                pass

            try:
                record['instrument'] = row['instrument_name'].decode('utf-8')
            except:
                pass

            results.append(record)

        return results


    # custom serializer for the 'query' endpoint
    class CreateAndRunQuerySerializer(serializers.Serializer):
        dataset = serializers.CharField()
        # dataset_name = serializers.CharField()
        result = serializers.CharField()
        dataproduct_type = serializers.CharField()
        calibration_level = serializers.IntegerField()
        target = serializers.CharField()
        obs_collection = serializers.CharField()
        size = serializers.IntegerField()
        ra = serializers.FloatField()
        dec = serializers.FloatField()
        fov = serializers.FloatField()
        facility = serializers.CharField()
        instrument = serializers.CharField()
        url = serializers.CharField()

        class Meta:
            fields = '__all__'
