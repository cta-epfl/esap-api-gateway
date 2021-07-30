import logging
from urllib.parse import quote_plus as quote_url
from rest_framework import generics, pagination
from rest_framework.response import Response
from ida.api.services import ida_controller
from django.views.generic import ListView
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from ida.models import *
from rest_framework import generics
from ..serializers import *
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class IdaViewSet(viewsets.ModelViewSet):
    serializer_class = IdaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.staging.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# example: /esap/ida/
class IndexView(ListView):
    queryset = Ida.objects.all()
    serializer_class = IdaSerializer
    template_name = 'ida/index.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_ida'


# example: /esap-api/facilities/search
class SearchFacilities(generics.ListAPIView):
    """
    Get a list of facilities that match a keyword search
    If no keyword provided, return all facilities
    examples:
    /esap-api/ida/facilities/search?keyword=SKA
    """

    model = Facility
    queryset = model.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        keyword = None

        # is there a keyword parameter?
        try:
            keyword = self.request.query_params['keyword']
        except:
            pass

        data = ida_controller.search_facilities(keyword=keyword, objectclass="facility")

        # paginate the results
        page = self.paginate_queryset(data)
        serializer = FacilitySerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)





# example: /esap-api/workflows/search
class SearchWorkflows(generics.ListAPIView):
    """
    Get a list of facilities that match a keyword search
    If no keyword provided, return all facilities
    examples:
    /esap-api/ida/workflows/search?keyword=SKA
    """

    model = Workflow
    queryset = model.objects.all()

    # override list and generate a custom response
    def list(self, request, *args, **kwargs):

        keyword = None

        # is there a keyword parameter?
        try:
            keyword = self.request.query_params['keyword']

        except:
            pass

        data = ida_controller.search_workflows(keyword=keyword, objectclass="workflow")

        # paginate the results
        page = self.paginate_queryset(data)
        serializer = WorkflowSerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)

# example: /esap-api/deploy
class Deploy():
    """
    Deploys workflows at compute facilities

    examples:
    /esap-api/ida/deploy?facility=https://mybinder.org/&amp;workflow=https://github.com/stvoutsin/esap_demo
    """

    def deploy(request, workflow=None, facility=None):
        """Deploy the specified workflow on the given facility.

        Note that the workflow is ignored unless the facility is MyBinder.

        Note also that workflow and facility paramters to this function appear
        to be entirely ignored in favour of looking at the request.
        """

        facility = Facility.objects.get(url=request.GET['facility'])
        workflow = Workflow.objects.get(url=request.GET['workflow'])

        if facility.name == "MyBinder":

            BINDER_API_ROOT = "https://mybinder.org/v2"
            BINDER_REPO_TYPE = "git"
            BINDER_REPO_URL = quote_url(workflow.url)
            BINDER_REPO_REF = workflow.ref
            BINDER_REPO_FILE = quote_url(workflow.filepath)

            # By default, launch into the JupyterLab environment
            BINDER_INTERFACE = f"urlpath=lab{'/tree/' + BINDER_REPO_FILE if BINDER_REPO_FILE else ''}"

            target = f"{BINDER_API_ROOT}/{BINDER_REPO_TYPE}/{BINDER_REPO_URL}/{BINDER_REPO_REF}?{BINDER_INTERFACE}"

        else:
            # Note that we're not actually using the workflow at all here --
            # it's just ignored as we redirect to the facility only.
            target = facility.url

        return redirect(target)

