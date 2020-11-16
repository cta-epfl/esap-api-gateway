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
    :param keyword: comma separated keywords
    :return:
    """
    
    return search(Workflow, keyword, objectclass)





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


