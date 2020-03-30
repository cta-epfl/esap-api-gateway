"""
    File name: vo.py
    Author: Nico Vermaas - Astron
    Date created: 2020-03-30
    Description:  ESAP services for Helio.

    # http://msslkz.mssl.ucl.ac.uk/helio-dpas/HelioQueryServlet?STARTTIME=2017-10-30T12:00:00&ENDTIME=2017-10-30T15:00:00&INSTRUMENT=SOHO__EIT
    # event catalog: http://hec.helio-vo.eu/hec/hec_gui.php

    # Data Provider Access Service
    # http://helio-vo.eu/services/interfaces/helio-dpas_uix2.php

    # http://helio-vo.eu/services/interfaces/helio-dpas_soap4.php?qtype=1&y_from=2017&mo_from=10&d_from=30&h_from=12&mi_from=00&s_from=00&interval=3.0&use_groups=select_bytype&obsinst_key%5B%5D=SOHO__EIT&obsinst_group=GONG__HALPH%2COACT__HALPH%2CKANZ__HALPH%2CCUCS__HASTA%2CMITK__HALPH%2CHIDA__SMART%2CHSOS__HALPH%2CKSAC__SHELIO%2CBBSO__HALPH%2CMEUD__SHELIO&operation=1&plot_type=&cxs_node=helio.mssl.ucl.ac.uk&cxs_process=dpas_findprocess&format=html&process=1

"""

from .query_base import query_base
import io,requests, json

from datetime import datetime

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

            # temp dirty hack to add time
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

        return query, errors


    def run_query(self, dataset, query):
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

            from astropy.io.votable import parse_single_table

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
                record['result'] = result

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
            record['result'] =  str(error)
            results.append(record)

        return results