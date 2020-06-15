from rest_framework import routers

from .views import StagingViewSet

router = routers.DefaultRouter()
router.register('staging', StagingViewSet, 'staging')

urlpatterns = router.urls