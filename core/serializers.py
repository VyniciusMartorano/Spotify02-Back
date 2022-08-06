from rest_framework import serializers
from .models import Musics

class MusicsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    file = serializers.FileField(use_url=True)

    class Meta:
        model = Musics
        fields = ('__all__')

    def create(self, validated_data):
        return Musics.objects.create(**validated_data)