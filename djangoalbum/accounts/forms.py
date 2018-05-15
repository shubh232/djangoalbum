from django import forms
from .models import AccountProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class UserRegis(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']


class ProfileForm(forms.ModelForm):
    """Update form for users profile."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields to include User properties."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["First Name"] = forms.CharField(
            initial=self.instance.user.first_name)
        self.fields["Last Name"] = forms.CharField(
            initial=self.instance.user.last_name)
        self.fields["Email"] = forms.EmailField(
            initial=self.instance.user.email)
        del self.fields["user"]

    class Meta:
        """Model for form and fields to exclude."""

        model = AccountProfile
        exclude = []
