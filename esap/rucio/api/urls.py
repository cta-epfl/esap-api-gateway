from rest_framework import routers

from .views import RucioViewSet

router = routers.DefaultRouter()
router.register('rucio', RucioViewSet, 'rucio')

urlpatterns = router.urls