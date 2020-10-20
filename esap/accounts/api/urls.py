from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"query-schemas", views.EsapQuerySchemaViewSet)
router.register(r"compute-resources", views.EsapComputeResourceViewSet)
router.register(r"software-repositories", views.EsapSoftwareRepositoryViewSet)
router.register(r"shopping-items", views.EsapShoppingItemViewSet)
router.register(r"user-profiles", views.EsapUserProfileViewSet)

urlpatterns = [path("", include(router.urls))]
