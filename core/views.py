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



class MusicsViewSet(viewsets.ModelViewSet):
    queryset = Musics.objects.all()
    serializer_class = MusicsSerializer


    @action(detail=False, methods=['post'])
    def download_music_by_url(self, *args, **kwargs):
        #TODO: LER ISSO
        """
        -Usar esta url como serviço...
        -Quando for salvar a musica como download deverá 
        pegar o path dela e armarzenar como string
        :Path da musica -> {MEDIA_ROOT}/musics/{filename}.mp3
        
        """
        req = self.request.data
        
        name_music = req['name_music'] if 'name_music' in req else None
        urlMusic = req['url'] if 'url' in req else None

        
        if not urlMusic: Response('A url da música não foi passado para a função') 
        
        try: 
            dowloadMusic(
                urlMusic=urlMusic, 
                output_path=f'{MEDIA_ROOT}/musics/' ,
                filename='2018-em-umaMusica',
                )
        except FileExistsError as erro: 
            return Response(data='A música que você está tentando inserir já existe em nosso banco de dados', status=status.HTTP_400_BAD_REQUEST)
        else: return Response(data='Download realizado com sucesso!', status=status.HTTP_200_OK)
        

      
            
        
    
    
    @action(methods=['delete'], detail=False)
    def delete(self, *args, **kwargs):
        request = self.request.data
        qs_artists = Artist.objects.all()
        qs_musics = Musics.objects.all()

        music_id = request['music_id'] if 'music_id' in request else None

        if not music_id: return Response(f'Não foi possivel deletar a música desejada',status=500)

        music = qs_musics.get(id=music_id)
        
        # artist_id = music.__dict__['artist_id'] 
        artist_id = music.artist.id 
        artist = qs_artists.filter(id=artist_id).first()
        #TODO: testar com get
        
        qs_artists.filter(id=artist_id).update(qtd_tracks=artist.__dict__['qtd_tracks'] - 1)
        music.delete()
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
