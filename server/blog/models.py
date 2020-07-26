from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .utils import unique_slugify
from editorjs_field.fields import EditorJSField

# Create your models here.

class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(max_length=250)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title