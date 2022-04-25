""" Extends the base URL patterns with the UWS endpoint """

from django.urls import include, path

from esap.urls import urlpatterns as base_patterns

base_patterns.append(path("esap-api/uws/", include("uws.urls")))

urlpatterns = base_patterns
