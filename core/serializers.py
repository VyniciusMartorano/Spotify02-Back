from rest_framework import serializers
from .models import Musics, Artist, Genero



class MusicsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Musics
        fields = ('__all__')


    def create(self, validated_data):
        qs_artists = Artist.objects.all()
        qs_musics = Musics.objects.all()
        artist = validated_data['artist'].__dict__ if 'artist' in validated_data else None

        if not artist: return Response('Não foi possivel criar a música desejada', 500)
        qs_artists.filter(id=artist['id']).update(qtd_tracks=artist['qtd_tracks'] + 1)
        return Musics.objects.create(**validated_data)



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('__all__')


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ('__all__')