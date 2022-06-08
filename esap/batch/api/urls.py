from django.urls import path
from django.contrib import admin
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('batch', views.BatchViewSet, 'batch')

urlpatterns = router.urls

urlpatterns = [
    path('', views.IndexView.as_view(), name='index-view'),
    # example: /esap-api/get-services?dataset=ivoa?keyword=ukidss
    path('facilities/search', views.SearchFacilities.as_view(), name='batch-facility-search'),
    path('workflows/search', views.SearchWorkflows.as_view(), name='batch-workflows-search'),
    #path('deploy', views.Deploy.deploy, name='deploy')
    path('CONCORDIA',views.ViewCONCORDIA.as_view(), name='concordia-view')
    
]


