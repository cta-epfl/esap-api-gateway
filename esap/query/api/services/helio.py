"""
    File name: helio.py
    Author: Nico Vermaas - Astron
    Date created: 2020-03-30
    Description:  ESAP services for Helio.

    # example
    # http://msslkz.mssl.ucl.ac.uk/helio-dpas/HelioQueryServlet?STARTTIME=2017-10-30T12:00:00&ENDTIME=2017-10-30T15:00:00&INSTRUMENT=SOHO__EIT

    # Data Provider Access Service
    # http://helio-vo.eu/services/interfaces/helio-dpas_uix2.php
"""

from .query_base import query_base
import requests
from astropy.io.votable import parse_single_table

AMP_REPLACEMENT = '_and_'

class helio_connector(query_base):
    """
    The connector to access HELIO
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):
        where = ''
        errors = []

        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            # temp dirty hack to add time.
            # Replace later with proper timestamp fields in the frontend
            if esap_key == 'startdate' or esap_key == 'enddate':
                value = value + "T00:00:00"

            try:
                dataset_key = translation_parameters[esap_key]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, then just continue without that key
                errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # cut off the last separation character
        where = where[:-len(AMP_REPLACEMENT)]

        query = self.url + '?' + where

        return query, where, errors


    def run_query(self, dataset, dataset_name, query):
        """
        :param dataset: the dataset object that must be queried
        :param query: the constructed query (that was probably generated with the above construct_query function)
        """

        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        try:
            # do the http request
            response = requests.request("GET", query)

            # the response is in VOTable format
            # write the contents to a file first, because astropy cannot parse xml as stream
            # also, xml in memory cannot be larger than the size of the memory.
            f = open('helio_votable.xml','w')
            f.write(response.text)
            f.close()

            # the VOTable from HELIO has the following fields.
            # instrument_name
            # provider_instrument
            # url
            # provider
            # time_start
            # time_end

            table = parse_single_table("helio_votable.xml")

            # iterate over the list of results..
            for table_rec in table.array:
                record = {}
                result = ''

                select_list = dataset.select_fields.split(',')
                for select in select_list:
                    try:
                        result = result + table_rec[select].decode("utf-8") + ','
                    except:
                        pass

                # cut off the last ','
                result = result[:-1]

                record['dataset'] = dataset.uri
                record['dataset_name'] = dataset_name
                record['result'] = result
                record['query'] = query

                try:
                    record['url'] = table_rec[dataset.url_field]
                except:
                    pass

                # some fields to return display information for the frontend.
                try:
                    # split off the filename from the path
                    filename = record['url'].decode("utf-8").rsplit('/',1)
                    record['title'] = filename[1] + '.fits'
                except:
                    pass

                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['dataset_name'] = dataset_name
            record['query'] = query
            record['result'] =  str(error)
            results.append(record)

        return results