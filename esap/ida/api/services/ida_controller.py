"""
    Business logic for ESAP-gateway.
    These functions are called from the 'views'.
"""

import json
import logging
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
    
    zenodo_workflows = Harvester.get_data_from_zenodo(query=keyword)

    logger.info("zenodo found %s workflows", len(zenodo_workflows))

    #TODO: * add annotations from KG. this allows to infer the keyword connections, 
    #TODO:   e.g. Mrk421 keyword will return references to blazar
    #TODO: * we can add ranking 
    #TODO: * parameter substitutions: some workflows may be manufactured on request
    #TODO: * keywords may be derived from context. note the difference between contextualization and personalization

    response["results"].extend(zenodo_workflows)
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


