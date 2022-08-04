from django.urls import path, include
from . import views as v
from rest_framework import routers


router = routers.DefaultRouter()
router.register('musics', v.MusicsViewSet)


urlpatterns = router.urls