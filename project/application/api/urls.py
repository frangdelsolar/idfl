from rest_framework import routers
from application.api.views import ApplicationViewSet

router = routers.DefaultRouter()
router.register('applications', ApplicationViewSet) 

urlpatterns = router.urls