from django.shortcuts import render
from django.views.generic import CreateView,ListView,DetailView
from .forms import UserRegis,ProfileForm
from .models import AccountProfile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView



PROFILE_TEMPLATE_PATH = 'profile.html'
# Create your views here.
class Profile(LoginRequiredMixin, ListView):
    """The user profile view."""

    login_url = reverse_lazy('login')

    model = User
    template_name = PROFILE_TEMPLATE_PATH

class Regis(CreateView):
    form_class = UserRegis
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class EditProfile(LoginRequiredMixin, UpdateView):
    """Edit users profile."""

    login_required = True
    template_name = 'edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return logged in users profile."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save object after post."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
