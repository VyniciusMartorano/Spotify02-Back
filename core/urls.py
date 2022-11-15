from django.urls import path, include
from . import views as v
from rest_framework import routers


router = routers.DefaultRouter()
router.register('musics', v.MusicsViewSet)
router.register('artist', v.ArtistViewSet)
router.register('genero', v.GeneroViewSet)
router.register('user', v.UserViewSet)
router.register('musicsliked', v.MusicsLikedViewSet)
router.register('playlist', v.PlaylistViewSet)
router.register('playlistmusic', v.PlaylistMusicViewSet)


urlpatterns = router.urls