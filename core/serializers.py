from rest_framework import serializers
from .models import Musics

class MusicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musics
        fields = ('__all__')