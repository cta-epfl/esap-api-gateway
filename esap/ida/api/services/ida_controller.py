"""
    Business logic for ESAP-gateway.
    These functions are called from the 'views'.
"""

import json
import logging
import typing

import requests
from ida.models import *
from django.db.models import Q
import django_filters
import collections
from . import Harvester

logger = logging.getLogger(__name__)


def search_facilities(keyword="", objectclass=""):
    """
    Search the known facilities for a given keyword
    :param keyword: comma separated keywords
    :return:
    """
    return search(Facility, keyword, objectclass)


WorkflowDict = typing.Dict
WorkflowList = typing.List[WorkflowDict]


def kg_select(s, p):
    #TODO: take statically update location instead
    r = requests.get("https://www.astro.unige.ch/mmoda/dispatch-data/gw/odakb/query", 
                params={"query": f"""
                    SELECT * WHERE {{
                        <{s}> <{p}> ?o .
                    }} LIMIT 100
                """}).json()
    
    logger.warning(r)

    return [result['o']['value'] for result in r['results']['bindings']]


# move elsewhere
class EnrichWorkflows:
    def __init__(self, workflows) -> None:
        self.workflows = workflows
        self.keyword_annotations = {}

    def do(self) -> WorkflowList:
        for workflow in self.workflows:
            self.add_keywords(workflow)
            self.annotate_keywords(workflow)
            
        return self.workflows
    
    def add_keywords(self, workflow: WorkflowDict) -> None:
        workflow_uri = workflow['url'] # TODO: add file?
        
        for k in kg_select(workflow_uri, "https://schema.org/keywords"):
            workflow['keywords'] += "," + k

    def annotate_keyword(self, keyword: str):
        logger.warning("annotate_keyword: %s", keyword)

    def annotate_keywords(self, workflow: WorkflowDict):
        for keyword in workflow['keywords'].split(","):
            self.annotate_keyword(keyword)

        

def search_workflows(keyword="", objectclass=""):
    """
    Search known workflows for a given keyword
    Harvests from the ESCAPE WP3 Zenodo repository and from local database
    :param keyword: comma separated keywords
    :return:
    """
    response = {}
    response["description"] = "ESAP API Gateway"
    response["requested_page"] = "1"
    response["requested_page_size"] = None
    response["max_page_size"] = 500
    response["default_page_size"] = "ESAP API Gateway"
    response["count"] = 0
    response["pages"] = 1
    response["results"] = []

    from django.core import serializers
    db_workflows = serializers.serialize("python", Workflow.objects.all())
    for db_entry in db_workflows:
        response["results"].append(db_entry["fields"])
    
    #TODO: potentially can instead change th eossr
    zenodo_workflows = [] #Harvester.get_data_from_zenodo(query=keyword)

    logger.warning("zenodo found %s workflows", len(zenodo_workflows))
    
    #TODO: * add annotations from KG. this allows to infer the keyword connections, 
    #TODO: * we can add ranking  when selecting by keyword
    #TODO: * parameter substitutions: some workflows may be manufactured on request
    #TODO: * keywords may be derived from context. note the difference between contextualization and personalization
    #TODO: * auto-generate notebooks to fetch MMODA
    #TODO: * KG represents, in additon to "native" zenodo tags
    #TODO:   * connections between keywords/entities (e.g. Mrk421 => blazar, blazar => agn, cta => cherenkov telescope). these links can be shown
    #TODO:   * own representation of inferred keywords with weights,
    #TODO:     trying our own idea of contextualized view without changing the "trhurh"
    #TODO:   * paper references? can be derived from zenodo too
    #TODO:   * executions which are not published in zenodo, should they really be?


    response["results"].extend(zenodo_workflows)
    
    EnrichWorkflows(response["results"]).do()

    return response



def search(model, keyword="", objectclass=""):
    """
    Search the known facilities for a given keyword
    :param keyword: comma separated keywords
    :return:
    """

    def apply_search(keyword, model, objectclass):
        if objectclass.lower()=="workflow":
            results = model.objects.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(url__icontains=keyword) 
            )
        if objectclass.lower()=="facility":
            #results  = model.objects.filter(name__contains=keyword).filter(description__contains=keyword).filter(url__contains=keyword)
            results = model.objects.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(url__icontains=keyword) 
            )

        return results
    
    
    results = []
    
    try:
        if keyword:
            results = apply_search(keyword, model, objectclass)
        else:
            results = model.objects.all()
            
    except Exception as error:
        record = {}
        record['result'] =  str(error)
        results.append(record)
        return results
 
    return results


