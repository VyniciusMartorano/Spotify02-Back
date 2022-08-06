from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets



class MusicsViewSet(viewsets.ModelViewSet):
    queryset = Musics.objects.all()
    serializer_class = MusicsSerializer


    @action(methods=['post'], detail=False)
    def retrieve_musics(self, request):
        qs = Musics.objects.all()
        return Response(request)

