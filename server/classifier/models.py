from django.core.files.base import ContentFile
from django.db import models

# Create your models here.

class Classifier(models.Model):
    document = models.FileField(upload_to='file/')
