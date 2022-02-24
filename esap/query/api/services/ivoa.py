"""
    File name: vo_reg.py
    Author: Nico Vermaas - Astron
    Date created: 2020-04-09
    Description:  ESAP services for VO registry
"""
from collections import namedtuple
from .query_base import query_base
from rest_framework import serializers
import pyvo
import urllib.parse

# available service types for VO
service_type_list = ['tap','sia','ssa','scs']

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


class vo_registry_connector(query_base):

    # Initializer
    def __init__(self, url):
        self.url = url

        # cut off the '/sync' resource, because the vo.dal.TAPServices will add it again
        if self.url.endswith('/sync'):
            self.url = self.url[:-4]

    # === helper functions ===

    # return the VO service based on service_type and access_url
    def get_service(self,access_url, service_type="TAP"):
        if service_type==None:
            service_type="TAP"

        if 'SCS' in service_type.upper():
            service = pyvo.dal.SCSService(access_url)
        elif 'SIA' in service_type.upper():
            service = pyvo.dal.SIAService(access_url)
        elif 'SSA' in service_type.upper():
            service = pyvo.dal.SSAService(access_url)
        elif 'TAP' in service_type.upper():
            service = pyvo.dal.TAPService(access_url)
        return service


    # Search for a keyword
    def search(self, keyword=None, service_type=None, datamodel=None, waveband=None, **kwargs):
        """
        # Use pyvo to do a Registry search by keyword
        :param keyword: The keyword to search for
        :param servicetype: The service type that we are searching for (e.g. tap)
        """

        try:
            keywords = keyword.split(',')
        except:
            keywords = None

        if datamodel:
            services = pyvo.registry.search(datamodel=datamodel)
        else:
            if waveband:
                services = pyvo.registry.search(keywords=keywords, servicetype=service_type, waveband=waveband)
            else:
                services = pyvo.registry.search(keywords=keywords, servicetype=service_type)

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

        return standards[service["standard_id"].lower()] if service["standard_id"] else None


    # === interface functions, called from the API ===

    # construct a query for this type of service
    def construct_query(self, dataset, query_params, translation_parameters, override_resource=None):

        esap_query_params = dict(query_params)
        where = ''
        errors = []

        # cone search is a specific type of query that uses ra, dec and a search radius.
        # it is also done with a specific ADQL syntax.
        # First check if the incoming query describes a cone search.

        cone_search = create_cone_search(esap_query_params,translation_parameters)

        for esap_param in esap_query_params:

            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                # skip pagination parameters
                # they are not 'esap parameters', and not used in VO
                if not esap_key in ['page', 'page_size']:
                    dataset_key = translation_parameters[esap_key]
                    where = where + dataset_key + "='" + value + "' "
                else:
                    # translate ESAP pagination parameters to VO pagination parameters
                    # page and page_size => TOP and OFFSET
                    pass

            except Exception as error:
                # if the parameter could not be translated, use it raw and continue
                where = where + esap_key + "='" + value + "' "
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))


        query = self.url + '/sync'

        # add pagination parameters
        # if no page_size is given, then set it here for ALTA, because ALTA default uses 500
        if not "page_size" in where:
            page_size = 50

        # add fixed ADQL parameters
        query_params = {}
        query_params["LANG"] = "ADQL"
        query_params["REQUEST"] = "doQuery"

        # if the parameter '&resource=...' is given to the url, then use that resource..
        # todo: temporarily using TOP 250 until we have implemented pagination from the VO service
        # SELECT TOP 50 () OFFSET 50
        if override_resource:
            query_params["QUERY"] = "SELECT TOP 250 * from " + override_resource
        else:
            # ... otherwise use the resource as defined in the datasets
            query_params["QUERY"] = "SELECT TOP 250 * from " + dataset.resource_name

        # add ADQL where where
        if where:
            if len(where)>0:
                query_params["QUERY"] += " WHERE " + where

        if cone_search:
            if len(cone_search)>0:
                if len(where)>0:
                    query_params["QUERY"] += " AND " + cone_search
                else:
                    query_params["QUERY"] += " WHERE " + cone_search

        query = query  + "?" + urllib.parse.urlencode(query_params)


        return query, where, errors


    # run a query
    def run_query(self, dataset, dataset_name, query,
                  session=None,
                  override_access_url=None,
                  override_service_type=None):
        """
        # use pyvo to do a vo query
        :param dataset: the dataset object that contains the information about the catalog to be queried
        :param query: the constructed (adql) query (that was probably generated with the above construct_query function)
        :param override_access_url: overrides access_url from the dataset
        :param override_service_type: overrides service_type from the dataset
        """

        results = []

        # The default service that the vo_reg dataset connects to is 'vo_reg.vo_registry_connector',
        # as specified in the 'service_connector' field of the dataset.
        # To query other catalogs, the 'override_access_url' can be used.

        # The default service_type = TAP, which can also be overridden with 'override_service_type'
        #service = vo.dal.TAPService(self.url)

        try:
            service = self.get_service(access_url=self.url,service_type="TAP")
            if override_access_url:
                service = self.get_service(access_url=override_access_url, service_type=override_service_type)

            # SELECT TOP 10 * from ivoa.obscore WHERE CONTAINS(POINT('ICRS',s_ra,s_dec), CIRCLE('ICRS',10.16,10.94,1.0))=1
            # SELECT+TOP+10+%2A+from+ivoa.obscore+WHERE+CONTAINS%28POINT%28%27ICRS%27%2Cs_ra%2Cs_dec%29%2C+CIRCLE%28%27ICRS%27%2C342.16%2C33.94%2C10.0%29%29%3D1
            q = urllib.parse.unquote(query).replace("+"," ")
            resultset = service.search(q)

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
            record['result'] = result
            record['query'] = query

            try:
                fieldnames = []
                for column in resultset.fieldnames:
                    new_column = {}
                    new_column['name'] = column
                    new_column_meta = resultset.getdesc(column)
                    new_column['description'] = new_column_meta.description
                    new_column['ucd'] = new_column_meta.ucd
                    new_column['utype'] = new_column_meta.utype
                    new_column['datatype'] = new_column_meta.datatype
                    fieldnames.append(new_column)
                record['fields'] = fieldnames
            except Exception as e:
                record['fields'] = ''

            # add some fields to return some rendering information for the frontend.
            # for ivoa.obscore field names see: http://www.ivoa.net/documents/ObsCore/20170509/REC-ObsCore-v1.1-20170509.pdf

            # We'll map field "src" in the result to field "dst" in the output
            # record. If "src" doesn't exist, we'll use "default" if specified,
            # otherwise we won't set the field.
            KeywordMapping = namedtuple('KeywordMapping', ['src', 'dst', 'default'])
            keyword_mappings = [
                KeywordMapping(dataset.title_field, 'title', None),
                KeywordMapping(dataset.thumbnail_field, 'thumbnail', None),
                KeywordMapping(dataset.url_field, 'url', '')
            ]
            for mapping in keyword_mappings:
                if mapping.src in row:
                    record[mapping.dst] = row[mapping.src]
                elif mapping.default is not None:
                    record[mapping.dst] = mapping.default

            results.append(record)

        return results


   # retrieve all the vo services that satisfy the given parameters
    def get_services(self, service_type, waveband, keyword):
        """
        # get all available services from the VO registry based on the keyword and possible a service_type
        :param service_type
        :param waveband
        :param keyword single keyword or comma separated list of keywords
        """

        results = []

        try:
            services = self.search(keyword, service_type=service_type, waveband=waveband)

        except Exception as error:
            return "ERROR: "+str(error)

        for resource in services:
            # see row attributes
            # https://pyvo.readthedocs.io/en/latest/api/pyvo.registry.regtap.RegistryResource.html#pyvo.registry.regtap.RegistryResource

            result = {}

            # VO RegistryResource attributes
            result['id'] = str(resource.standard_id)
            result['title'] = str(resource.res_title)
            result['service_type'] = str(resource.res_type)
            result['access_url'] = str(resource.access_url)

            result['short_name'] = resource.short_name
            result['content_types'] = str(resource.content_types)
            result['waveband'] = ' '.join([str(elem) for elem in resource.waveband])

            # result['description'] = str(resource.res_description)
            # result['content_levels'] = str(resource.content_levels)
            # result['creators'] = str(resource.creators)
            # result['ivoid'] = str(resource.ivoid)
            # result['reference_url'] = str(resource.reference_url)
            # result['region_of_regard'] = str(resource.region_of_regard)
            # result['source_format'] = str(resource.source_format)

            results.append(result)

        return results


    # retrieve the fields of a service (get-tap-schema in VO speak)
    def get_tables_fields(self, dataset, access_url):
        """
        # get all available services from the VO registry based on the keyword and possible a service_type
        :param service_type
        :param waveband
        :param keyword
        """

        tables = []

        try:
            # query = "select+*+from+TAP_SCHEMA.schemas"
            # query = "select+*+from+TAP_SCHEMA.tables"
            # query = "select+*+from+TAP_SCHEMA.columns+where+table_name='II/336/apass9'"

            service = self.get_service(access_url, "TAP")
            for table in service.tables:
                my_table = {}
                my_table['table_name'] = table.name
                my_table['table_type'] = table.type

                my_columns = []
                for column in table.columns:
                    my_column = {}
                    my_column['name'] = column.name
                    my_column['description'] = column.description
                    my_column['unit'] = column.unit
                    my_column['datatype'] = column.datatype.content
                    my_columns.append(my_column)

                my_table['fields'] = my_columns

                tables.append(my_table)

        except Exception as error:
            return "ERROR: " + str(error)

        return tables


    # custom serializer for the 'query' endpoint
    class CreateAndRunQuerySerializer(serializers.Serializer):

        dataset = serializers.CharField()
        result = serializers.CharField()
        query = serializers.CharField()
        url = serializers.CharField()
        thumbnail = serializers.CharField()

        # extra fields
        fields = serializers.ListField()

        class Meta:
            fields = '__all__'
