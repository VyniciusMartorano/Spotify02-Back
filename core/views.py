from django.shortcuts import render
import sys
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
sys.path.append('utils')
from utils.dowloadMusic import dowloadMusic



class MusicsViewSet(viewsets.ModelViewSet):
    queryset = Musics.objects.all()
    serializer_class = MusicsSerializer

    def post(self, request, format=None):
        print(f'\n{request.data}\n')
        req = request.data
        urlMusic = req['url']
        music = dowloadMusic(urlMusic)
        req['file'] = music
        print(f'\n{request.data}\n')

        serializer = MusicsSerializer(data=req)

        if serializer.is_valid():
            serializer.save(
                image=request.data.get['image']
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['post'], detail=False)
    def retrieve_musics(self, request):
        qs = Musics.objects.all()
        return Response(request)




