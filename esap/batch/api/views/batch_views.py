import logging
from urllib.parse import quote_plus as quote_url
from rest_framework import generics, pagination
from rest_framework.response import Response
from batch.api.services import batch_controller
from django.views.generic import ListView
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions
from batch.models import *
from rest_framework import generics
from ..serializers import *
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class BatchViewSet(viewsets.ModelViewSet):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.staging.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# example: /esap/batch/
class IndexView(ListView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    template_name = 'batch/index.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_batch'


# example: /esap-api/facilities/search
class SearchFacilities(generics.ListAPIView):
    """
    Get a list of facilities that match a keyword search
    If no keyword provided, return all facilities
    examples:
    /esap-api/batch/facilities/search?keyword=SKA
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

        data = batch_controller.search_facilities(keyword=keyword, objectclass="facility")

        # paginate the results
        page = self.paginate_queryset(data)
        serializer = FacilitySerializer(instance=page, many=True)

        return self.get_paginated_response(serializer.data)



# example: /esap-api/workflows/search
class SearchWorkflows(APIView):
    """
    Get a list of facilities that match a keyword search
    If no keyword provided, return all facilities
    examples:
    /esap-api/batch/workflows/search?keyword=SKA
    """

    model = Workflow
    queryset = model.objects.all()

    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head']


    def get(self, request, keyword=None):
        keyword = None

        # is there a keyword parameter?
        try:
            keyword = self.request.query_params['keyword']

        except:
            pass

        data = batch_controller.search_workflows(keyword=keyword, objectclass="workflow")
        return Response(data)

    def post(self, request, keyword=None):
        keyword = None

        # is there a keyword parameter?
        try:
            keyword = self.request.query_params['keyword']

        except:
            pass

        data = batch_controller.search_workflows(keyword=keyword, objectclass="workflow")
        return Response(data)

class ViewCONCORDIA(ListView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    template_name = 'batch/concordia.html'

    # by default this returns the list in an object called object_list, so use 'object_list' in the html page.
    # but if 'context_object_name' is defined, then this returned list is named and can be accessed that way in html.
    context_object_name = 'my_batch'


