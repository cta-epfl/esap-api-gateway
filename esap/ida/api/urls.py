from django.urls import path
from django.contrib import admin
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('ida', views.IdaViewSet, 'ida')

urlpatterns = router.urls

urlpatterns = [
    path('', views.IndexView.as_view(), name='index-view'),
    path('my_ida', views.StagingListViewAPI.as_view(), name='ida-view'),
    # example: /esap-api/get-services?dataset=ivoa?keyword=ukidss
    path('facilities/search', views.SearchFacilities.as_view()),
    path('workflows/search', views.SearchWorkflows.as_view()),
    path('deploy', views.Deploy.deploy)
    
]

