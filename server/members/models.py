from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import ValidationError


# Create your models here.

class UserLink(models.Model):
    """
    A single directed edge in the social graph.  Usually represented as the
    verb "follows".

    """
    from_user = models.ForeignKey(User, related_name='following_links', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_links', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return u"%s is following %s" % (self.from_user.username,
                                        self.to_user.username)

    def save(self, **kwargs):
        """
        A mostly-generic save method, except that it validates that the user
        is not attempting to follow themselves.
        """
        if self.from_user == self.to_user:
            raise ValueError("Cannot follow yourself.")
        super(UserLink, self).save(**kwargs)

    class Meta:
        unique_together = (('to_user', 'from_user'),)


class Profile(models.Model):
    USERNAME = "username"
    FULLNAME = "full name"
    NAME_CHOICES = (
        (USERNAME, 'Username'),
        (FULLNAME, 'Full name'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2000, blank=True)
    photo = models.ImageField(upload_to="users/avatars/", default="users/avatars/default.jpg", blank=True)
    banner = models.ImageField(upload_to="users/banners/", default="users/banners/default.jpg", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    profile_name = models.CharField(max_length=10, choices=NAME_CHOICES, default=USERNAME)

    @property
    def get_profile_name(self):
        if self.profile_name == self.USERNAME:
            return self.user.username
        return "{} {}".format(self.user.first_name, self.user.last_name)
        pass

    def __str__(self):
        return "Profile for user {}".format(self.user.username)


# signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()