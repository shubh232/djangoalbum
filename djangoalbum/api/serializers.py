from django.contrib.auth.models import User
from rest_framework import serializers

from albums.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('url','title','description','user','photos','cover')
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','email')
