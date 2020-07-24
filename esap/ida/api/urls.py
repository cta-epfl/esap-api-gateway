from django.urls import path
from django.contrib import admin
from rest_framework import routers

from .views import IdaViewSet
from . import views

router = routers.DefaultRouter()
router.register('ida', IdaViewSet, 'ida')

urlpatterns = router.urls

urlpatterns = [
    path('admin', admin.site.urls, name='admin-view'),
    path('', views.IndexView.as_view(), name='index-view'),
    path('my_ida', views.StagingListViewAPI.as_view(), name='ida-view'),
]

