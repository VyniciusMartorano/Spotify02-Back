from django.db import models



class Musics(models.Model):
    music_name = models.CharField(max_length=255, null=False, blank=False)
    artist = models.CharField(max_length=255, null=False, blank=False)
    genero = models.CharField(max_length=100, null=False, blank=False)
    file = models.FileField(upload_to='', null=True)
    image = models.ImageField()
    duration = models.FloatField(null=False, blank=False)
    liked = models.BooleanField(null=False, blank=False)

    def __str__(self): return self.music_name

    class Meta:
        managed = False
        db_table = 'Musics'