from django.urls import path, include
from . import views as v
from rest_framework import routers


router = routers.DefaultRouter()
router.register('musics', v.MusicsViewSet)
router.register('artist', v.ArtistViewSet)
router.register('genero', v.GeneroViewSet)


urlpatterns = router.urls