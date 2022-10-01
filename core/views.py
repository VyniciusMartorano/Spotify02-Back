from django.shortcuts import render
import sys
from rest_framework import viewsets
from .models import Musics, Artist, Genero
from .serializers import MusicsSerializer, ArtistSerializer, GeneroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
sys.path.append('utils')
from utils.dowloadMusic import dowloadMusic
from api.settings import MEDIA_ROOT
from utils.media.media_urls import DEFAULT_IMAGE_PATH
import os





class MusicsViewSet(viewsets.ModelViewSet):
    queryset = Musics.objects.all()
    serializer_class = MusicsSerializer
 
    
    @action(detail=False, methods=['post'])
    def insert_music(self, *args, **kwargs):
        fields = [ 'name_music','artist_id','genero_id','image','music_url', 'music_file']
        name_music, artist_id, genero_id, image, music_url, music_file = [ self.request.data.get(item, None) for item in fields ]

        if not music_url and not music_file: return Response(data='Você precisa enviar a música', status=500)

        if music_url and music_file: return Response(data='Você deve enviar apenas um dos dois formatos', status=400)

        if not image: image = DEFAULT_IMAGE_PATH
        print('\n',image)

        music = music_file or music_url

        if type(music) == str: 
            try: 
                dowloadMusic(
                    urlMusic=music, 
                    output_path=f'{MEDIA_ROOT}/musics/',
                    filename=name_music,
                )
                music = f'musics/{name_music}.mp3'
            except FileExistsError: return Response(f'A música {name_music} já existe no banco de dados', status=400)
            except Exception as e: return Response(f'Não foi possivel salvar a música')

        music = Musics(
            music_name=name_music,
            artist_id=artist_id,
            genero_id=genero_id,
            file=music,
            image=image
        )
        music.save(force_insert=True)
        return Response(MusicsSerializer(music).data)
        


        
    @action(methods=['delete'], detail=False)
    def delete(self, *args, **kwargs):
        request = self.request.data
        qs_artists = Artist.objects.all()
        qs_musics = Musics.objects.all()

        music_id = request['music_id'] if 'music_id' in request else None
        if not music_id: return Response(f'Não foi possivel deletar a música desejada',status=500)

        music = qs_musics.get(id=music_id)
        artist_id = music.artist.id 
        artist = qs_artists.filter(id=artist_id).first()
        #TODO: testar com get
        
        qs_artists.filter(id=artist_id).update(qtd_tracks=artist.__dict__['qtd_tracks'] - 1)
        try: music.delete()
        except: return Response(data=f'Não foi possivel deletar a música {music.__dict__["music_name"]}')
        else: 
            os.remove(f'{MEDIA_ROOT}/{music.__dict__["file"]}')
            return Response(f'A música {music.__dict__["music_name"]} foi deletada com sucesso', status=200)

        
    @action(methods=['post'], detail=False)
    def search(self, *args, **kwargs):
        request = self.request.data
        queryset = Musics.objects.all()

        data_filter = request['data_filter'] if 'data_filter' in request else None

        if data_filter:
            queryset = queryset.filter(music_name__icontains=data_filter) |\
            queryset.filter(artist__name__icontains=data_filter)

        return Response(MusicsSerializer(queryset, many=True).data) 


    @action(methods=['post'], detail=False)
    def retrieve_musics(self, *args, **kwargs):
        request = self.request.data
        queryset = Musics.objects.all()
        
        artist_name = request['artist_name'] if 'artist_name' in request else None
        music_name = request['music_name'] if 'music_name' in request else None

        if artist_name:
            queryset = queryset.filter(artist__name__icontains=artist_name)
        
        if music_name:
            queryset = queryset.filter(music_name__icontains=music_name)

        return Response(MusicsSerializer(queryset, many=True).data, status=200)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
