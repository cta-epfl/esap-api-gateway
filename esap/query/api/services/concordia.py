"""
    File name: concordia.py
    Date created: 2022-01-10
    Description:  DIRAC Service Connector for ESAP.
"""
import time
from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script
from DIRAC.Interfaces.API.Job import Job
from DIRAC.Interfaces.API.Dirac import Dirac
from rest_framework import serializers
from .query_base import query_base
import requests
import json
import logging
import string

logger = logging.getLogger(__name__)

AMP_REPLACEMENT = "_and_"

# --------------------------------------------------------------------------------------------------------------------


class concordia_connector(query_base):
    """
    The connector to use WP3's CONCORDIA
    """

    # Initializer
    def __init__(self, url):
        self.url = url

    # construct a query 
    def construct_query(
        self, dataset, esap_query_params, translation_parameters
    ):

        query = {'jobid': 'empty'}
        where = {}
        error = {}


        if 'jobid' in esap_query_params.keys():
              query['jobid'] =  str(esap_query_params.pop('jobid')[0])

        logger.info("__________________________________PARAMS " + str(query))

        return query, where, error

    def _get_data_from_concordia(self, query, session):

        results = {}

# HERE IS WHERE THE CONCORDIA CODE GOES
# EXAMPLE:

        concordia = Dirac()
        j = Job()

        j.setCPUTime(500)
        j.setExecutable('/bin/echo hello')
        j.setExecutable('/bin/hostname')
        j.setExecutable('/bin/echo hello again')
        j.setName('API')

# Let us not bother a computer everytime I hit refresh for now
        if query['jobid'] == 'empty'  or query['jobid'] == 'undefined':
          jobID = concordia.submitJob(j)
          time.sleep(2)
          tempID = jobID['Value']
          statusID = concordia.getJobStatus(tempID)
        else:
          tempID = query['jobid']
          statusID = concordia.getJobStatus(tempID)


# Here is some output I made earlier
        if query['jobid'] == 'empty' or query['jobid'] == 'undefined':
          #jobID = {'JobID': 18544353, 'OK': True, 'Value': 18544353, 'requireProxyUpload': False, 'rpcStub': [['WorkloadManagement/JobManager', {'delegatedDN': None, 'delegatedGroup': None, 'timeout': 600, 'skipCACheck': True, 'keepAliveLapse': 150}], 'submitJob', ['[ \n    Arguments = "jobDescription.xml -o LogLevel=INFO";\n    CPUTime = 500;\n    Executable = "dirac-jobexec";\n    InputSandbox = \n        {\n            "SB:ProductionSandboxSE|/SandBox/g/ghughes.cta_user/84a/846/84a846e906bf49ed981c7821d720a260.tar.bz2"\n        };\n    JobGroup = vo.cta.in2p3.fr;\n    JobName = Hello World;\n    JobType = User;\n    LogLevel = INFO;\n    OutputSandbox = \n        {\n            Script1_CodeOutput.log,\n            std.err,\n            std.out\n        };\n    Priority = 1;\n    StdError = std.err;\n    StdOutput = std.out;\n]']]}
          #time.sleep(2)
          #statusID = {'OK': True, 'Value': {18544353: {'ApplicationStatus': 'Unknown', 'MinorStatus': 'Job Initialization', 'Status': 'Running', 'Site': 'LCG.IN2P3-CC.fr'}}}
          results['JobID'] = jobID['JobID']
          temp = jobID['JobID']
          results['OK'] = statusID['OK']
          results['MinorStatus'] = statusID['Value'][temp]['MinorStatus']
          results['Status'] = statusID['Value'][temp]['Status']
          results['Site'] = statusID['Value'][temp]['Site']
        else:
          #statusID = {'OK': True, 'Value': {18544353: {'ApplicationStatus': 'echo successful', 'MinorStatus': 'Execution Complete', 'Status': 'Done', 'Site': 'LCG.IN2P3-CC.fr'}}}
          results['JobID'] = query['jobid']
          temp = int(query['jobid'])
          results['OK'] = statusID['OK']
          results['MinorStatus'] = statusID['Value'][temp]['MinorStatus']
          results['Status'] = statusID['Value'][temp]['Status']
          results['Site'] = statusID['Value'][temp]['Site']


        #logger.info("Submission: " + str(jobID))

        #if query != "empty":
            #try:
                 #response = get_zenodo_records(**query)
            #except:
                 #logger.info("No Results Found in Zenodo Archive Search")
        #else:
             #logger.info("Empty search in Zenodo Archive Search")

        #if len(response) > 0:
            #results = [
                #element.data
                #for element in response
             #]

        results = [ results ]

        #logger.info("-----------------TYPE!!!!: " + str(type(results)))
        #logger.info("Result: " + str(results))

        return results

        #return jobID

    def run_query(
        self,
        dataset,
        dataset_name,
        query,
	session,
        override_access_url=None,
        override_service_type=None,
    ):
        """
        :param dataset: the dataset object that must be queried
        :param query_params: the incoming esap query parameters)
        :return: results: an array of dicts with the following structure;
        """

        # create a function that reads the data from lofar
        concordia_results = self._get_data_from_concordia(query, session)

        return concordia_results

    # custom serializer for the 'query' endpoint

    class TypeToSerializerMap:

        map = {
            type(float): serializers.FloatField(),
            type(int): serializers.IntegerField(),
            type(str): serializers.CharField(),
            type(dict): serializers.DictField(),
            type(list): serializers.ListField(),
        }

        @classmethod
        def getFieldForType(cls, value):
            return cls.map.get(type(value), serializers.JSONField())

    class CreateAndRunQuerySerializer(serializers.Serializer):
        """
        Custom serializer classes implement dynamic field definition based on
        the contents of the query passed to it.
        """

        def __init__(self, *args, **kwargs):

            self.example_result = kwargs.get("instance", [])[0]

            super().__init__(*args, **kwargs)

            self.fields.update(
                {
                    key: concordia_connector.TypeToSerializerMap.getFieldForType(value)
                    for key, value in self.example_result.items()
                }
            )
