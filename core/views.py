from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class MusicsViewSet(ModelViewSet):
    queryset = Musics.objects.all()
    serializer_class = MusicsSerializer