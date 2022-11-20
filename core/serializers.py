from rest_framework import serializers
from . import models as m
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        
        return user



class MusicsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    file = serializers.FileField(use_url=True)

    class Meta:
        model = m.Musics
        fields = ('__all__')


    def create(self, validated_data):
        qs_artists = m.Artist.objects.all()
        qs_musics = m.Musics.objects.all()
        artist = validated_data['artist'].__dict__ if 'artist' in validated_data else None

        if not artist: return Response('Não foi possivel criar a música desejada', 500)
        qs_artists.filter(id=artist['id']).update(qtd_tracks=artist['qtd_tracks'] + 1)
        return m.Musics.objects.create(**validated_data)



class MusicsLikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.MusicsLiked
        fields = ('__all__')



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Artist
        fields = ('__all__')



class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Genero
        fields = ('__all__')



class PlaylistSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)
    
    class Meta:
        model = m.Playlist
        fields = ('__all__')



class PlaylistMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PlaylistMusic
        fields = ('__all__')



class PlaylistGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PlaylistGroup
        fields = ('__all__')



class PlaylistGroupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PlaylistGroupItem
        fields = ('__all__')