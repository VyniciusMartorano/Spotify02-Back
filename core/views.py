import sys, os
sys.path.append('utils')
from django.shortcuts import render
import json
from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from utils.dowloadMusic import dowloadMusic
from api.settings import MEDIA_ROOT 
from utils.media.media_urls import DEFAULT_IMAGE_PATH
from . import  models as m
from . import serializers as s




"""
TODO:

QUANDO CRIAR ARTISTA JA CRIAR A PLAYLIST THIS DELE
E QUANDO FOR ADICIONADA UMA MUSICA JA ADICIONAR ELA NA PLAYLIST THIS
usar trigger pra isso




TODO: CRIAR API PARA DOWNLOADS
"""



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = s.UserSerializer

    
    @action(detail=False, methods=['post'])
    def create_user(self, *args, **kwargs):
        queryset = User.objects
        req = self.request.data

        fields = ['name', 'email', 'password']
        name, email, password = [ req.get(item, None) for item in fields ]

        if not (name and email and password):
            return Response(f'Envie todos os campos (name, email, password)', status=400)
        
        try:
            user = User.objects.create(
                username=name,
                first_name=name,
                email=email,
                is_active=True,
                is_superuser=False
            )
            user.set_password(password)
            user.save()
        except Exception as e: return Response(f'Ocorreu um erro ao salvar o usuario {e}', status=400)
        else: return Response({"name": name})


    @action(detail=False, methods=['post'])
    def login(self, *args, **kwargs):
        req = self.request.data

        fields = ['username', 'password']
        username, password = [ req.get(item, None) for item in fields ]

        if not username: return Response('O username não pode estar vazio', status=400)
        if not password: return Response('A senha não pode estar vazia', status=400)
        
        user = authenticate(username=username, password=password)

        if user is not None: 
            return Response('Autenticação realizada com sucesso', status=200)
        else: 
            return Response(f'Usuario ou senha inválido', status=400)
    

    @action(detail=False, methods=['post'])
    def logout(self, *args, **kwargs):
        req = self.request
        print(req)



        return Response('Logout realizado com sucesso', status=200)




class ArtistViewSet(viewsets.ModelViewSet):
    queryset = m.Artist.objects.all()
    serializer_class = s.ArtistSerializer
    


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = m.Genero.objects.all()
    serializer_class = s.GeneroSerializer



class MusicsViewSet(viewsets.ModelViewSet):
    queryset = m.Musics.objects
    serializer_class = s.MusicsSerializer
 
    
    @action(detail=False, methods=['post'])
    def insert_music(self, *args, **kwargs):
        qs_musics = m.Musics.objects
        fields = [ 'name_music','artist_id','genero_id','image','music_url', 'music_file']
        name_music, artist_id, genero_id, image, music_url, music_file = [ self.request.data.get(item, None) for item in fields ]

        if not music_url and not music_file: return Response(data='Você precisa enviar a música', status=400)
        if music_url and music_file: return Response(data='Você deve enviar apenas um dos dois formatos', status=400)
        if not image: 
            image = DEFAULT_IMAGE_PATH
    
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
        else:
            if (qs_musics.filter(music_name=name_music).count() > 0):
                return Response(data=f'A música {name_music} já existe no banco de dados', status=400)

        music = m.Musics(
            music_name=name_music,
            artist_id=artist_id,
            genero_id=genero_id,
            file=music,
            image=image
        )
        music.save()
        return Response(s.MusicsSerializer(music).data)
        
        
    @action(methods=['delete'], detail=False)
    def delete(self, *args, **kwargs):
        """
            ? This function delete the music and update qtd_tracks of artist
            @param music_id
        """
        request = self.request.data
        qs_artists = m.Artist.objects.all()
        qs_musics = m.Musics.objects.all()

        music_id = request['music_id'] if 'music_id' in request else None
        if not music_id: return Response(f'Você precisa enviar o id da música para a deleção',status=500)
        try: music = qs_musics.get(id=music_id)
        except: return Response('Não foi possivel encontrar a música no banco de dados', status=500)

        artist = qs_artists.filter(id=music.artist.id).first()
        if artist.qtd_tracks > 0: qs_artists.filter(id=music.artist.id).update(qtd_tracks=artist.qtd_tracks - 1)

        try: music.delete()
        except: return Response(data=f'Não foi possivel deletar a música {music.music_name}')
        else: 
            os.remove(f'{MEDIA_ROOT}/{music.file}')
            if music.image != DEFAULT_IMAGE_PATH:
                os.remove(f'{MEDIA_ROOT}/{music.image}')
            return Response(f'A música {music.music_name} foi deletada com sucesso', status=200)

        
    @action(methods=['post'], detail=False)
    def search(self, *args, **kwargs):
        request = self.request.data
        queryset = m.Musics.objects.all()

        data_filter = request['data_filter'] if 'data_filter' in request else None

        if data_filter:
            queryset = queryset.filter(music_name__icontains=data_filter) |\
            queryset.filter(artist__name__icontains=data_filter)

        return Response(s.MusicsSerializer(queryset, many=True).data) 


    @action(methods=['post'], detail=False)
    def retrieve_musics(self, *args, **kwargs):
        request = self.request.data
        queryset = m.Musics.objects.all()
        
        artist_name = request['artist_name'] if 'artist_name' in request else None
        music_name = request['music_name'] if 'music_name' in request else None

        if artist_name: queryset = queryset.filter(artist__name__icontains=artist_name)
        
        if music_name: queryset = queryset.filter(music_name__icontains=music_name)

        return Response(s.MusicsSerializer(queryset, many=True).data, status=200)



class MusicsLikedViewSet(viewsets.ModelViewSet):
    queryset = m.MusicsLiked.objects.all()
    serializer_class = s.MusicsLikedSerializer



class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = m.Playlist.objects.all()
    serializer_class = s.PlaylistSerializer


    @action(detail=False, methods=['post'])
    def retrieve_playlists(self, *args, **kwargs):
        qs = m.Playlist.objects.using('default')
        queryset = self.request.data

        user_id = req['user_id'] if 'user_id' in req else None
        isDefault = req['isDefault'] if 'isDefault' in req else None


        if user_id: qs = qs.filter(user_id=user_id)
        if isDefault: qs = qs.filter(isDefault=isDefault)

        return Response(s.PlaylistSerializer(qs, many=True).data, status=200)

    def get_playlists_ids_by_group_id(self, group_id) -> list:
        qs_playlist_group_itens = m.PlaylistGroupItem.objects.using('default')
        qs_playlists = m.Playlist.objects.using('default')

        ids_playlists = qs_playlist_group_itens.filter(group_id=group_id).values_list('playlist_id')
        qs_playlists = qs_playlists.filter(id__in=ids_playlists)

        return s.PlaylistSerializer(qs_playlists, many=True).data


    @action(detail=False, methods=['get'])
    def retrieve_playlists_by_groups(self, *args, **kwargs):
        qs_groups = m.PlaylistGroup.objects.using('default').all()

        result = []

        for group in qs_groups:
            group_playlists = {}
            group_playlists['id'] = group.id
            group_playlists['title'] = group.descricao
            group_playlists['playlists'] = self.get_playlists_ids_by_group_id(group.id)

            result.append(group_playlists)



        serializado = json.dumps({'data': result})

        return Response(result, status=200)



class PlaylistGroupViewSet(viewsets.ModelViewSet):
    queryset = m.PlaylistGroup.objects.all()
    serializer_class = s.PlaylistGroupSerializer



class PlaylistGroupItemViewSet(viewsets.ModelViewSet):
    queryset = m.PlaylistGroupItem.objects.all()
    serializer_class = s.PlaylistGroupItemSerializer



class PlaylistMusicViewSet(viewsets.ModelViewSet):
    queryset = m.PlaylistMusic.objects.all()
    serializer_class = s.PlaylistMusicSerializer


