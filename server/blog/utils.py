from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.utils import timezone

def unique_slugify(title):
    slug = slugify(unidecode(title))
    return "{}-{}".format(slug, timezone.now().strftime("%j%H%M%S%f"))