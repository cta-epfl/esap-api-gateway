from django.urls import path
from django.contrib import admin
from rest_framework import routers

from .views import StagingViewSet
from . import views

router = routers.DefaultRouter()
router.register('staging', StagingViewSet, 'staging')

urlpatterns = router.urls

urlpatterns = [
    # path('admin', admin.site.urls, name='admin-view'),
    path('', views.IndexView.as_view(), name='index-view'),
    path('staging', views.StagingListViewAPI.as_view(), name='staging-view'),
]

