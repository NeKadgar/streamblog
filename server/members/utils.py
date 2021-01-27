from django.contrib.auth.models import User
from members.models import UserLink
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from pathlib import Path


def get_people_user_follows(user):
    """
    Returns a ``QuerySet`` representing the users that the given user follows.
    """
    ul = UserLink.objects.filter(from_user=user).values_list('to_user', flat=True)
    return User.objects.filter(id__in=ul)


def get_followers_count(user):
    count = UserLink.objects.filter(to_user=user).values_list('to_user', flat=True).count()
    return count


def is_following(from_user, to_user):
    follow_status = UserLink.objects.filter(from_user=from_user, to_user=to_user).exists()
    return follow_status


def get_people_following_user(user):
    """
    Returns a ``QuerySet`` representing the users that follow the given user.
    """
    ul = UserLink.objects.filter(to_user=user).values_list('from_user', flat=True)
    return User.objects.filter(id__in=ul)


def is_email_correct(email=None):
    if email and not User.objects.filter(email=email).exists():
        try:
            validate_email(email)
        except ValidationError:
            return False
        else:
            return True
    return False


def is_image_correct(image):
    if not image:
        return False
    allowed_extension = [
        "jpg",
        "jpeg",
        "png"
    ]
    max_size = 8.0
    extension = Path(image.name).suffix[1:].lower()
    if extension in allowed_extension:
        limit = max_size * 1024 * 1024
        if image.size < limit:
            return True
    return False
