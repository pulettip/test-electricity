from django.conf.urls import url

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()
router.register(r'buildings', views.BuildingViewSet)
router.register(r'meters', views.MetersViewSet)
router.register(r'readings', views.MetersReadingsViewSet)

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)