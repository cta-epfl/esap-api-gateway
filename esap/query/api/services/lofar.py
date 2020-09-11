"""
    File name: lofar.py
    Date created: 2020-08-28
    Description:  LOFAR Service Connector for ESAP.
"""

from astropy.coordinates import SkyCoord
import math
import datetime
from awlofar.main.aweimports import CorrelatedDataProduct, \
    AveragingPipeline, \
    Observation, FileObject, \
    SubArrayPointing, Pointing
from awlofar.database.Context import context
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


def get_data_from_lofar(query):
    """ use awlofar library to query Lofar LTA """

    # parse query string, e.g. target_name, ra, dec, ...
    target_name = "A2255"
    dataproduct_type = "AveragingPipeline"
    antenna_type = "HBA"
    public = "true"  # query public data only

    # convert object name to sky coordinates
    # target_coords = SkyCoord.from_name(target_name)
    # Resolved coordinates is
    # <SkyCoord (ICRS): (ra, dec) in deg
    # (258.2085, 64.05294444)>
    # target_coords.ra.deg, target_coords.dec.deg
    # target_coords.ra.rad, target_coords.dec.rad

    # Given (ra, dec) in deg (258.2085, 64.05294444)
    # construct lta query
    target_coords = SkyCoord.from_name("A2255")
    results = []
    observations = set()
    lta_query = (Pointing.rightAscension > math.floor(target_coords.ra.deg)) &\
        (Pointing.rightAscension < math.floor(target_coords.ra.deg+1)) &\
        (Pointing.declination > math.floor(target_coords.dec.deg)) &\
        (Pointing.declination < math.floor(target_coords.dec.deg+1))

    for pointing in lta_query:
        print("Pointing found RA %f DEC %f" %
              (pointing.rightAscension, pointing.declination))
        query_obs = Observation.subArrayPointings.contains(
            SubArrayPointing.pointing == pointing)
        for obs in query_obs:
            observations.add(obs)

    # for obs in observations:
    #     print(obs.observationId, obs.observingMode)
    #     "HBA" in obs.antennaSet
    #     "A2255" in obs.observationDescription

    for obs in observations:
        dataproducts = AveragingPipeline.sourceData.contains(
            CorrelatedDataProduct.observations.contains(obs))
        dataproducts &= AveragingPipeline.isValid == 1
        for dataproduct in dataproducts:
            result = {"project": obs.projectInformation.projectCode, "sas_id": obs.observationId, "antennaSet": obs.antennaSet,
                      "instrumentFilter": obs.instrumentFilter, "target": obs.observationDescription,
                      "startTime": obs.startTime, "duration": obs.duration,
                      "releaseDate": dataproduct.releaseDate, "pipeline": dataproduct.pipelineName,
                      "ra": obs.subArrayPointings[1].pointing.rightAscension,
                      "dec": obs.subArrayPointings[1].pointing.declination}
            results.append(result)

    print(results)

    return list(results)


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
        print("ESAP Lofar query params:", esap_query_params)

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

    def run_query(self, dataset, dataset_name, query, override_access_url=None, override_service_type=None):
        """
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;
        """
        print("query:", query)
        results = []

        # create a function that reads the data from lofar
        #lofar_results = get_data_from_lofar(query)

        # database connection is not working, copied results returned from get_data_from_lofar(query)
        lofar_results = [
            {'project': 'LC12_027', 'sas_id': '727108', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 7, 3, 18, 0, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '727108', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 7, 3, 18, 0, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '751364', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 11, 15, 9, 11), 'duration': 29140.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '751364', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 11, 15, 9, 11), 'duration': 29140.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '747611', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 10, 4, 12, 41, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '747611', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 10, 4, 12, 41, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '746862', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 9, 28, 12, 0, 1), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '746862', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 9, 28, 12, 0, 1), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '725452', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 22, 19, 0, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '725452', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 22, 19, 0, 1), 'duration': 29170.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '726706', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 28, 18, 0, 1), 'duration': 30060.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '726706', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 28, 18, 0, 1), 'duration': 30060.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '733075', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 8, 9, 16, 30), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '733075', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 8, 9, 16, 30), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '720376', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 7, 20, 3, 59), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '720376', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 6, 7, 20, 3, 59), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC0_037', 'sas_id': '122880', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255_11042013/A2255/1/TO (Target Observation)',
             'startTime': datetime.datetime(2013, 4, 11, 18, 49, 1), 'duration': 0.0, 'releaseDate': datetime.datetime(2015, 3, 1, 0, 0), 'pipeline': 'A2255_11042013/4C+64', 'ra': 259.998403, 'dec': 64.076898},
            {'project': 'LC12_027', 'sas_id': '728072', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 7, 8, 17, 51, 1), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'EDS-N/1.2/TP', 'ra': 258.2085, 'dec': 64.05294444444444},
            {'project': 'LC12_027', 'sas_id': '728072', 'antennaSet': 'HBA Dual Inner', 'instrumentFilter': '110-190 MHz', 'target': 'A2255EDSREF/1/TO (Target Observation)',
             'startTime': datetime.datetime(2019, 7, 8, 17, 51, 1), 'duration': 29180.0, 'releaseDate': datetime.datetime(2020, 11, 26, 0, 0), 'pipeline': 'A2255/1.1/TP', 'ra': 258.2085, 'dec': 64.05294444444444}]

        try:
            for lofar_result in lofar_results:
                record = {}

                record['project'] = lofar_result['project']
                record['sas_id'] = lofar_result['sas_id']
                record['antennaSet'] = lofar_result['antennaSet']
                record['instrumentFilter'] = lofar_result['instrumentFilter']
                record['target'] = lofar_result['target']
                record['startTime'] = lofar_result['startTime']
                record['duration'] = lofar_result['duration']
                record['releaseDate'] = lofar_result['releaseDate']
                record['pipeline'] = lofar_result['pipeline']
                record['ra'] = lofar_result['ra']
                record['dec'] = lofar_result['dec']

                results.append(record)

        except Exception as error:
            return "ERROR: " + str(error)

        return results

    # custom serializer for the 'query' endpoint

    class CreateAndRunQuerySerializer(serializers.Serializer):

        # Zheng: this defines the structure of the response to /esap/query/query for LOFAR
        # the fields should be the same as in run-query

        project = serializers.CharField()
        sas_id = serializers.CharField()
        antennaSet = serializers.CharField()
        instrumentFilter = serializers.CharField()
        target = serializers.CharField()
        startTime = serializers.CharField()
        duration = serializers.CharField()
        releaseDate = serializers.CharField()
        pipeline = serializers.CharField()
        ra = serializers.FloatField()
        dec = serializers.FloatField()

        class Meta:
            fields = '__all__'
