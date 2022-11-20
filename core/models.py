from django.db import models
from PIL import Image
from pickletools import optimize
import os
from django.conf import settings
from django.contrib.auth.models import User


def upload_image_music(instance, filename):
    return f'images/{instance}-{filename}'

def upload_thumbnail(instance, filename):
    return f'images/thumbnails/{instance}-{filename}'

def upload_file_music(instance, filename):
    return f'musics/{instance}-{filename}'


class Artist(models.Model):
    name       = models.CharField(max_length=255, null=False, blank=False)
    qtd_tracks = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'Artists'
    
    def __str__(self):
        return self.name



class Genero(models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=100)

    class Meta:
        managed = False
        db_table = 'Generos'
    
    def __str__(self):
        return self.descricao



class Musics(models.Model):
    music_name = models.CharField(max_length=100, null=False, blank=False)
    artist     = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genero     = models.ForeignKey(Genero, on_delete=models.CASCADE)
    image      = models.ImageField(db_column='imagem',upload_to=upload_image_music, blank=True)
    file       = models.FileField(db_column='music',upload_to=upload_file_music, blank=True)
    duration   = models.FloatField(null=True, blank=True)
    #TODO: trazer a info do liked no serializer puxando do musicsliked

    def __str__(self): return self.music_name
    
    @staticmethod
    def resize_image(img, new_width=68):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height_rounded = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height_rounded), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
    
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        max_image_size = 68
        if self.image: self.resize_image(self.image, max_image_size)
       


    class Meta:
        managed = False
        db_table = 'Musics'


class MusicsLiked(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    music_id = models.ForeignKey(Musics, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'MusicsLiked'
        


class Playlist(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    descricao = models.CharField(max_length=45, null=False, blank=False)
    user_id = models.ForeignKey(User, db_column='user_id',on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=upload_thumbnail, blank=True)
    is_default = models.IntegerField(null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'Playlists'
    
    def __str__(self): return self.title



class PlaylistMusic(models.Model):
    music_id = models.ForeignKey(Musics, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(Playlist,db_column='playlist_id' ,on_delete=models.CASCADE)


    class Meta:
        managed = False
        db_table = 'PlaylistMusic'



class PlaylistGroup(models.Model):
    descricao = models.CharField(max_length=20, blank=False, null=False)
    default = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'PlaylistGroups'
    
    def __str__(self): return self.descricao


class PlaylistGroupItem(models.Model):
    playlist_id = models.ForeignKey(Playlist,db_column='playlist_id' ,on_delete=models.CASCADE)
    group_id = models.ForeignKey(PlaylistGroup,db_column='group_id' ,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'PlaylistGroupItens'



