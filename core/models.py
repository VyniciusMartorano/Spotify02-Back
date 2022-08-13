from django.db import models
from PIL import Image
from pickletools import optimize
import os
from django.conf import settings


def upload_image_music(instance, filename):
    return f'images/{instance}-{filename}'

def upload_file_music(instance, filename):
    return f'musics/{instance}-{filename}'


class Musics(models.Model):
    music_name = models.CharField(max_length=255, null=False, blank=False)
    artist = models.CharField(max_length=255, null=False, blank=False)
    genero = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to=upload_image_music)
    file = models.FileField(upload_to=upload_file_music)
    duration = models.FloatField(null=False, blank=False)
    liked = models.BooleanField(null=False, blank=False)

    def __str__(self): return self.music_name

    @staticmethod
    def resize_image(img, new_width=68):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        max_image_size = 68
        if self.image:
            self.resize_image(self.image, max_image_size)

    class Meta:
        managed = False
        db_table = 'Musics'

        