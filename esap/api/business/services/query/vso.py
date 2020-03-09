"""
    File name: vso.py
    Author: Nico Vermaas - Astron
    Date created: 2020-03-06
    Description:  ESAP services for Virtual Solar Observatory

    Documentation:
    - https://virtualsolar.org/cgi-bin/search?help=1
"""

from .query_base import query_base
import requests, json
from datetime import datetime

AMP_REPLACEMENT = '_and_'

class vso_connector(query_base):
    """
    The connector to access the VSO
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service
    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

        where = ''
        errors = []

        # loop through the list of input parameters and translate them.
        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]

                # some specific VSO business logic to construct the timerange.
                # Convert the ESAP values to a VSO timerange
                if dataset_key=="start":
                    start_date = datetime.strptime(value, "%Y-%m-%d").strftime("%Y%m%d")
                elif dataset_key=="end":
                    end_date = datetime.strptime(value, "%Y-%m-%d").strftime("%Y%m%d")
                else:
                    # because '&' has a special meaning in urls (specifying a parameter) replace it with
                    # something harmless during serialization.
                    where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, then just continue without this parameter
                errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # cut off the last separation character
        where = where[:-len(AMP_REPLACEMENT)]

        # construct the query url by first adding the constructed timerange, followed by the rest of the parameters
        timerange="timerange="+start_date+"-"+end_date
        where = timerange + "_and_" + where

        query = self.url + '?' + where

        return query, errors



    def run_query(self, dataset, query):
        """
        :param dataset: the dataset object that must be queried
        :param query: the constructed query (that was probably generated with the above construct_query function)
        :return: results: an array of dicts with the following structure;

        example:
        /esap-api/run-query/?dataset_uri=vso&query=https://sdac.virtualsolar.org/cgi/vsoui?timerange=20040107-20040108_and_instrument=eit&waverange=304

        {
            "dataset": "vso",
            "result": "SDAC,SOHO",
            "title": "/archive/soho/private/data/processed/eit/lz/2004/01/efz20040106.235333",
            "url": "/archive/soho/private/data/processed/eit/lz/2004/01/efz20040106.235333"
        },
        {
            "dataset": "vso",
            "result": "SDAC,SOHO",
            "title": "/archive/soho/private/data/processed/eit/lz/2004/01/efz20040107.001148",
            "url": "/archive/soho/private/data/processed/eit/lz/2004/01/efz20040107.001148"
        },


        """
        results = []

        # because '&' has a special meaning in urls (specifying a parameter) it had been replaced with
        # something harmless during serialization. Replace it again with the &
        query = query.replace(AMP_REPLACEMENT,'&')

        try:

            # execute the first http request to ALTA to do the cone search on observation level.
            response = requests.request("GET", query)
            json_response = json.loads(response.text)
            resultset = json_response["resultset"]

            # iterate over the list of results..
            for json_record in resultset:
                record = {}
                result = ''

                select_list = dataset.select_fields.split(',')
                for select in select_list:
                    try:
                        result = result + json_record[select] + ','
                    except:
                        pass

                # cut off the last ','
                result = result[:-1]

                record['dataset'] = dataset.uri
                record['result'] = result

                # some fields to return display information for the frontend.
                try:
                    record['title'] = json_record[dataset.title_field]
                except:
                    pass

                try:
                    # hardcoded thumbnail field, because it is in the deeper 'extra' structure of the json.
                    extra = json_record['extra']
                    record['thumbnail'] = extra['thumbnail']
                except:
                    pass

                try:
                    record['url'] = json_record[dataset.url_field]
                except:
                    pass

                results.append(record)

        except Exception as error:
            record['dataset'] = dataset.uri
            record['result'] =  str(error)
            results.append(record)

        return results