from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .utils import unique_slugify
import jsonfield


# Create your models here.

class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(max_length=230)
    content = jsonfield.JSONField()
    description = models.TextField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    preview_image = models.ImageField(upload_to="posts/preview/", default="posts/preview/default.jpg")
    post_views = models.IntegerField(default=0)

    @property
    def views_count(self):
        return PostViews.objects.filter(post=self).count()

    def get_name_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)
        return tags

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        post = self.post
        post.post_views = post.post_views + 1
        post.save()
        super(PostViews, self).save(*args, **kwargs)


class BaseImage(models.Model):
    image = models.ImageField(upload_to="base/images/")
    name = models.CharField(max_length=50)


class Image(models.Model):
    image = models.ImageField(upload_to="posts/images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url