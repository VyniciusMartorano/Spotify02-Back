from django.db import models


def upload_image_music(instance, filename):
    return f'images/{instance.id}-{filename}'

def upload_file_music(instance, filename):
    return f'musics/{instance.id}-{filename}'


class Musics(models.Model):
    music_name = models.CharField(max_length=255, null=False, blank=False)
    artist = models.CharField(max_length=255, null=False, blank=False)
    genero = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to=upload_image_music)
    file = models.FileField(upload_to=upload_file_music)
    duration = models.FloatField(null=False, blank=False)
    liked = models.BooleanField(null=False, blank=False)

    def __str__(self): return self.music_name

    class Meta:
        managed = False
        db_table = 'Musics'