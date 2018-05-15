"""djangoalbum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import login,logout
from accounts.views import Regis,Profile,EditProfile
from albums.views import AddPhoto,PhotoView,AddAlbum,AlbumView,Library,DelPhoto,DelAlbum,EditPhoto,EditAlbum,AlbumsView,\
    PhotosView,PostLikePhoto,PostLikeAlbum
from rest_framework import routers

from api.views import AlbumAPI,UserViewSet

router = routers.DefaultRouter()
router.register(r'albums',AlbumAPI)
router.register(r'users',UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='home.html'),name='homepage'),
    path('accounts/register/',Regis.as_view(),name = 'register'),
    path('login/',login,name = 'login'),
    path('logout/',logout, {'next_page': '/'}, name='logout'),
    path('accounts/profile/',Profile.as_view(),name = 'profile'),
    path('edit/',EditProfile.as_view(),name =  'edit-profile'),
    path('photos/add/',AddPhoto.as_view(),name = 'AddPhoto'),
    path('albums/add/',AddAlbum.as_view(),name = 'AddAlbum'),
    path('albums/<int:album_id>/',AlbumView.as_view(),name = 'single_album'),
    path('albums/<int:album_id>/like/',PostLikeAlbum.as_view(),name = 'like_album'),
    path('albums/',AlbumsView.as_view(),name = 'public_album'),
    path('photos/',PhotosView.as_view(),name = 'public_photos'),
    path('photos/<int:photo_id>/',PhotoView.as_view(),name = 'single_photo'),
    path('photos/<int:photo_id>/like/', PostLikePhoto.as_view(), name='like_photo'),
    path('photos/<int:pk>/delete/',DelPhoto.as_view(),name = 'delete_photo'),
    path('photos/<int:pk>/edit/',EditPhoto.as_view(),name = 'edit_photo'),
    path('albums/<int:pk>/edit/', EditAlbum.as_view(), name='edit_album'),
    path('albums/<int:pk>/delete/', DelAlbum.as_view(), name='delete_album'),
    path('library/',Library.as_view(),name = 'library'),
    path('api/',include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
