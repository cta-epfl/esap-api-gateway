"""
    Business logic for ESAP-gateway.
    These functions are called from the 'views'.
"""

import copy
from email.policy import default
import json
import logging
import re
import typing

import requests
from ida.models import *
from django.db.models import Q
import django_filters
import collections
from . import Harvester

logger = logging.getLogger(__name__)

# TODO: this should be set on boot
logging.basicConfig(level=logging.INFO)


def search_facilities(keyword="", objectclass=""):
    """
    Search the known facilities for a given keyword
    :param keyword: comma separated keywords
    :return:
    """
    return search(Facility, keyword, objectclass)


WorkflowDict = typing.Dict
WorkflowList = typing.List[WorkflowDict]

def kg_select(t):
    #TODO: take statically update location instead
    r = requests.get("https://www.astro.unige.ch/mmoda/dispatch-data/gw/odakb/query", 
                params={"query": f"""
                    SELECT * WHERE {{
                        {t}
                    }} LIMIT 1000
                """}).json()

    return r['results']['bindings']


def kg_select_o(s, p):
    #TODO: take statically update location instead
    r = kg_select(f'<{s}> <{p}> ?o')

    return [result['o']['value'] for result in r]


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
        
        for k in kg_select_o(workflow_uri, "https://schema.org/keywords"):
            workflow['keywords'] += "," + k

    def annotate_keyword(self, keyword: str) -> str:
        logger.info("annotate_keyword: %s", keyword)

        if keyword not in self.keyword_annotations:
            def kg_select_sibling_by_label(label):
                def short_name(u):
                    return re.split("[#/]", u)[-1]
                
                S = [
                    [r['parent']['value'], r['sibling']['value']]
                    for r in kg_select(f'?a ?b "{label}"; a ?parent . ?sibling a ?parent') ]

                uris = set([r['a']['value'] for r in kg_select(f'?a ?b "{label}"') ])

                logger.info("found URIs: %s", uris)

                for s in S:
                    logger.info("found sibling result: %s", s)

                #/
                parent_fertility = collections.defaultdict(int)
                for p, s in S:
                    parent_fertility[p] += 1
                #/

                ordered_siblings = []      
                for sibling in set([sibling for parent, sibling in S]):
                    if short_name(sibling) == keyword: continue

                    logger.info("proximity %s %s", label, short_name(sibling))

                    total_weight = 10000
                    linking_parents = []
                    for p in [p for p, s in S if s == sibling]:
                        logger.info("for %s common parent %s", short_name(sibling), short_name(p))
                        total_weight = 1/(1/total_weight + parent_fertility[p])
                        linking_parents.append(short_name(p))

                    for uri in uris:
                        if [sibling, uri] in S:
                            logger.info("this sibling is also a parent!")
                            total_weight = 1/(1/total_weight + parent_fertility[sibling])


                    ordered_siblings.append([linking_parents, short_name(sibling), total_weight])

                return ordered_siblings
            
                # return [ [short_name(parent), short_name(sibling), parent_fertility[parent]]
                #          for parent, sibling in S]

            self.keyword_annotations[keyword] = kg_select_sibling_by_label(keyword)

            for s in self.keyword_annotations[keyword]:
                logger.info("found sibling: %s", s)
            
        return self.keyword_annotations[keyword]

    def annotate_keywords(self, workflow: WorkflowDict):
        new_keywords = []
        workflow['keyword_annotations'] = {}
        for keyword in workflow['keywords'].split(","):
            keyword_annotations = self.annotate_keyword(keyword) 
            workflow['keyword_annotations'][keyword] = keyword_annotations

            keyword_annotations_string = "; ".join([f"{k[1]} {k[2]:.2f}" for k in sorted(keyword_annotations, key=lambda x:x[2])])

            # new_keywords.append(keyword + f" ({keyword_annotations_string})")
            # TODO: need to also use length of links, not just number
            new_keywords.append(keyword)
            for k in sorted(keyword_annotations, key=lambda x:x[2]):
                new_keywords.append(f"{k[1]} ({k[2]:.2f})")
            
        
        workflow['keywords'] = ",".join(new_keywords)
            
        

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
    
    try:
        EnrichWorkflows(response["results"]).do()
    except Exception as e:
        logger.exception('failed to EnrichWorkflows %s', e)


    for result in response["results"]:
        result['class'] = 'regular'


    # add autogenerated workflows
    autogen_workflows = []

    for result in copy.deepcopy(response["results"]):
        result['class'] = 'autogen'
        autogen_workflows.append(result)

    # add autosaved workflows
    autosave_workflows = []

    for result in copy.deepcopy(response["results"]):
        result['class'] = 'autosave'
        autosave_workflows.append(result)

    response['results'].extend(autogen_workflows)
    response['results'].extend(autosave_workflows)

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


