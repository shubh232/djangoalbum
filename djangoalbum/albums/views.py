"""Views for images."""
from django.shortcuts import get_object_or_404

from .models import Photo,Album
from django.http import Http404
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

class AddPhoto(LoginRequiredMixin, CreateView):
    """Add a photo."""

    login_url = reverse_lazy('login')

    template_name = "add_photo.html"
    model = Photo
    fields = ['image', 'title', 'description', 'date_published', 'published']
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """Make the form user instance the current user."""
        form.instance.user = self.request.user
        return super(AddPhoto, self).form_valid(form)

class DelPhoto(DeleteView):
    """Delete View."""
    model = Photo
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('library')


class PhotoView(ListView):
    """Photo View."""

    model = Photo
    template_name = "photo.html"

    def get_context_data(self):
        user = self.request.user
        """Return photo."""
        photo = Photo.objects.get(id=self.kwargs['photo_id'])
        if photo.published != 'private' or photo.user.username == self.request.user.username:
            return {"photo": photo,'user':user}
        else:
            raise Http404('Unauthorized')
        return {}



class EditPhoto(LoginRequiredMixin, UpdateView):
    """Add a photo."""
    login_url = reverse_lazy('login')
    template_name = "add_photo.html"
    model = Photo
    fields = ['image', 'title', 'description', 'date_published', 'published']
    # success_url = '/images/library'
    success_url = reverse_lazy('library')


class AlbumView(ListView):
    """Album View."""

    model = Album
    template_name = "album.html"

    def get_context_data(self):
        """Return album."""
        album = Album.objects.get(id=self.kwargs['album_id'])
        if album.published != 'private' or album.user.username == self.request.user.username:
            photos = album.photos.all()
            cover = album.cover
            title = album.title
            id = album.pk
            like = album.likes.count
            date = album.date_created
            user = self.request.user
            this_page = self.request.GET.get("page", 1)
            pages = Paginator(photos, 4)

            try:
                photos = pages.page(this_page)
            except PageNotAnInteger:
                photos = pages.page(1)
            except EmptyPage:
                photos = pages.page(pages.num_pages)
            return {'photos': photos, 'cover': cover,'title':title,'date':date,'like':like,'user':user,'id':id}
        else:
            raise Http404('Unauthorized')
        return {}

class AddAlbum(LoginRequiredMixin, CreateView):
    """Add Album."""
    login_url = reverse_lazy('login')
    template_name = "add_album.html"
    model = Album
    fields = ['title', "cover", "description", "photos", "published", "date_published"]
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """Make the form user instance the current user."""
        form.instance.user = self.request.user
        return super(AddAlbum, self).form_valid(form)


class EditAlbum(LoginRequiredMixin, UpdateView):
    """Add Album."""

    template_name = "add_album.html"
    model = Album
    fields = ['title', "cover", "description", "photos", "published", "date_published"]
    success_url = reverse_lazy('library')


class DelAlbum(DeleteView):
    model = Album
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy('library')


class AlbumsView(TemplateView):
    """Albums View."""

    template_name = "albums.html"

    def get_context_data(self):
        """Return albums."""
        public_albums = []
        albums = Album.objects.all()
        for album in albums:
            if album.published != 'private':
                public_albums.append(album)
        this_page = self.request.GET.get("page", 1)
        pages = Paginator(public_albums, 4)

        try:
            public_albums = pages.page(this_page)
        except PageNotAnInteger:
            public_albums = pages.page(1)
        except EmptyPage:
            public_albums = pages.page(pages.num_pages)
        return {'albums': public_albums}

class PhotosView(TemplateView):
    """Photos View."""

    template_name = "photos.html"

    def get_context_data(self):
        """Return photos."""
        public_photos = [x for x in Photo.objects.filter(published='public')]
        this_page = self.request.GET.get("page", 1)
        pages = Paginator(public_photos, 4)

        try:
            photos = pages.page(this_page)
        except PageNotAnInteger:
            photos = pages.page(1)
        except EmptyPage:
            photos = pages.page(pages.num_pages)

        return {"photos": photos}



class Library(LoginRequiredMixin, TemplateView):
    """Library View."""

    login_url = reverse_lazy('login')

    template_name = "library.html"

    def get_context_data(self):
        """Return albums."""
        albums = self.request.user.albums.all()
        photos = self.request.user.photos.all()
        albums_page = self.request.GET.get("albums_page", 1)
        photos_page = self.request.GET.get("photos_page", 1)
        albums_pages = Paginator(albums, 4)
        photos_pages = Paginator(photos, 4)
        try:
            albums = albums_pages.page(albums_page)
            photos = photos_pages.page(photos_page)
        except PageNotAnInteger:
            albums = albums_pages.page(1)
            photos = photos_pages.page(1)
        except EmptyPage:
            albums = albums_pages.page(albums_pages.num_pages)
            photos = photos_pages.page(photos_pages.num_pages)
        return {'albums': albums, 'photos': photos}

class PostLikePhoto(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("photo_id")
        print(pk)
        obj = get_object_or_404(Photo,id=pk)
        print(obj.description)
        url = reverse_lazy('single_photo',kwargs={'photo_id':pk})
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url

class PostLikeAlbum(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("album_id")
        print(pk)
        obj = get_object_or_404(Album,id=pk)
        print(obj.description)
        url = reverse_lazy('single_album',kwargs={'album_id':pk})
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url