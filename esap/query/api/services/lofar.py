"""
    File name: lofar.py
    Date created: 2020-08-28
    Description:  LOFAR Service Connector for ESAP.
"""

from rest_framework import serializers
from .query_base import query_base
import requests
import json
import logging

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = '_and_'

# The request header
LTA_HOST = "https://https://lta.lofar.eu/"

# --------------------------------------------------------------------------------------------------------------------


class lta_connector(query_base):
    """
    The connector to access the LOFAR
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query for this type of service

    def construct_query(self, dataset, esap_query_params, translation_parameters, equinox):

        where = ''
        errors = []

        # translate the esap_parameters to specific catalog parameters
        for esap_param in esap_query_params:
            esap_key = esap_param
            value = esap_query_params[esap_key][0]

            try:
                dataset_key = translation_parameters[esap_key]

                # because '&' has a special meaning in urls (specifying a parameter) replace it with
                # something harmless during serialization.
                where = where + dataset_key + '=' + value + AMP_REPLACEMENT

            except Exception as error:
                # if the parameter could not be translated, use it raw and continue
                where = where + esap_key + "=" + value + AMP_REPLACEMENT
                logger.info("ERROR: could not translating key " +
                            esap_key + ' ' + str(error)+', using it raw.')
                # errors.append("ERROR: translating key " + esap_key + ' ' + str(error))

        # if query ends with a separation character then cut it off
        if where.endswith(AMP_REPLACEMENT):
            where = where[:-len(AMP_REPLACEMENT)]

        # Zheng, this is where you could change the format of the LOFAR query.
        # this is not required, you can also leave it like this.
        # The 'query' variable that is returned is already translated with the lofar parameter_mapping
        # here. I only used some example paramters, so you may still want to change the parameter_mapping.

        # construct the query url
        # for now simply like: 'https://lta.lofar.eu/?ra=342.16_and_dec=33.94_and_fov=10'
        query = self.url + '?' + where
        logger.info('construct_query: '+query)
        return query, where, errors

    def get_data_from_lofar(query):
        """ use awlofar library to query Lofar LTA """

        from astropy.coordinates import SkyCoord
        from awlofar.database.Context import context
        from awlofar.main.aweimports import CorrelatedDataProduct, \
            AveragingPipeline, \
            Observation, FileObject, \
            SubArrayPointing, Pointing
        import math

        results = []
        # parse query string, e.g. target_name, ra, dec, ...
        target_name = "A2255"
        dataproduct_type = "AveragingPipeline"
        antenna_type = "HBA"
        public = "true"  # query public data only

        # convert object name to sky coordinates

        target_coords = SkyCoord.from_name("A2255")
        # Resolved coordinates is
        # <SkyCoord (ICRS): (ra, dec) in deg
        # (258.2085, 64.05294444)>
        # target_coords.ra.deg, target_coords.dec.deg
        # target_coords.ra.rad, target_coords.dec.rad

        # Given (ra, dec) in deg (258.2085, 64.05294444) and fov 1.0
        # construct lta query
        observations = set()
        lta_query = (Pointing.rightAscension > math.floor(target_coords.ra.deg)) &\
            (Pointing.rightAscension < math.floor(target_coords.ra.deg+1)) &\
            (Pointing.declination > math.floor(target_coords.dec.deg)) &\
            (Pointing.declination < math.floor(target_coords.dec.deg+1))

        for pointing in lta_query:
            print("Pointing found RA %f DEC %f" %
                  (pointing.rightAscension, pointing.declination))
            query_subarr = SubArrayPointing.pointing == pointing
            for subarr in query_subarr:
                query_obs = Observation.subArrayPointings.contains(subarr)
                for obs in query_obs:
                    observations.add(obs)

            for obs in observations:
                print(obs.observationId, obs.observingMode)
                "HBA" in obs.antennaSet

            Observation.antennaSet.like("HBA Dual")

        cls = AveragingPipeline
        for obs in observations:
            dataproduct_query = AveragingPipeline.sourceData.contains(obs)
            # isValid = 1 means there should be an associated URI
            dataproduct_query &= AveragingPipeline.isValid == 1
            for dataproduct in dataproduct_query:
                print(dataproduct.centralFrequency,
                      dataproduct.creationDate, dataproduct.dataProductType,
                      dataproduct.releaseDate, dataproduct.subArrayPointing)

        observation = list(observations)[0]
        dataproduct_query = CorrelatedDataProduct.observations.contains(
            observation)
        dataproduct_query = AveragingPipeline.sourceData.contains(
            observation)
        dataproduct = dataproduct_query[0]

        return results

    def run_query(self, dataset, dataset_name, query, override_access_url=None, override_service_type=None):
        """
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;
        """

        results = []

        # Zheng: implement run_query functionality here,
        # you can use the incoming 'query' to find the requested parameters

        # create a function that reads the data from lofar
        # lofar_results = get_data_from_lofar(query)

        # fake example, something like this should come from your connection to LOFAR
        lofar_results = [
            {"name": "crap nebula", "sasid": "12345", "ra": "12.34",
                "dec": "56.78", "url": "https://https://lta.lofar.eu/"},
            {"name": "Nico's Star", "sasid": "12345", "ra": "12.34",
                "dec": "56.78", "url": "https://https://lta.lofar.eu/"},
            {"name": "Zheng's Voorwerp", "sasid": "12345", "ra": "12.34",
                "dec": "56.78", "url": "https://https://lta.lofar.eu/"},
        ]

        try:
            for lofar_result in lofar_results:
                record = {}

                record['name'] = lofar_result['name']
                record['sasid'] = lofar_result['sasid']
                record['ra'] = lofar_result['ra']
                record['dec'] = lofar_result['dec']
                record['url'] = lofar_result['url']

                results.append(record)

        except Exception as error:
            return "ERROR: " + str(error)

        return results

    # custom serializer for the 'query' endpoint

    class CreateAndRunQuerySerializer(serializers.Serializer):

        # Zheng: this defines the structure of the response to /esap/query/query for LOFAR
        # the fields should be the same as in run-query

        name = serializers.CharField()
        sasid = serializers.CharField()
        ra = serializers.FloatField()
        dec = serializers.FloatField()
        url = serializers.CharField()

        class Meta:
            fields = '__all__'
