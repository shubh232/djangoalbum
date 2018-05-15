from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from albums.models import Album
from api.serializers import AlbumSerializer
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserSerializer


class AlbumAPI(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

