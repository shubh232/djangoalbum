"""Models for imager_profile."""

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.management import create_permissions
from django.apps import apps


def image_path(instance, file_name):
    """Upload file to media root in user folder."""
    return 'user_{0}/{1}'.format(instance.user.id, file_name)


class ActiveProfileManager(models.Manager):  # pragma: no cover
    """Create Model Manager for Active Profiles."""

    def get_queryset(self):
        """Return active users."""
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class AccountProfile(models.Model):
    """The imager user and all their attributes."""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female') ]


    objects = models.Manager()
    active = ActiveProfileManager()

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    address = models.CharField(max_length=70, default="",blank=True)
    bio = models.TextField(default="",blank= True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,blank = True)
    personal_website = models.URLField(default="",blank=True)
    phone_number = models.CharField(max_length=20, default="",blank=True)



    @property
    def is_active(self):  # pragma: no cover
        """Return True if user associated with this profile is active."""
        return self.user.is_active

    def __str__(self):
        """Display user data as a string."""
        return "User: {}, Address: {}, Phone number: {}".format(self.user, self.address, self.phone_number  )


@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    """Called when user is made and hooks that user to a profile."""
    if kwargs["created"]:
        group = Group.objects.get(name="user")
        instance.groups.add(group)
        new_profile = AccountProfile(user=instance)
        new_profile.save()


@receiver(post_migrate)
def create_group(**kwargs):
    """On migration create group if it doesn't exists."""
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None
    group, created = Group.objects.get_or_create(name='user')
    imager_content_types = [x for x in ContentType.objects.filter(app_label='albums')]
    imager_content_types += [x for x in ContentType.objects.filter(app_label='accounts')]
    permissions = []
    for content_type in imager_content_types:
        permissions.extend([x for x in Permission.objects.filter(content_type=content_type)])
    if created:
        for permission in permissions:
            group.permissions.add(permission)
        group.save()
