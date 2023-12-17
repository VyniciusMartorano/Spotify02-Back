from django.contrib import admin
from . import models as m


# Register your models here.
admin.site.register(m.Musics)
admin.site.register(m.Pessoa)
admin.site.register(m.Album)
admin.site.register(m.AlbumMusic)