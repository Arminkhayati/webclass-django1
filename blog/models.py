from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    # A Manager for filtering all published posts
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = ... # a CharField with max_length=250
    slug = ... # a SlugField with max_length=250, and unique_for_date='publish'
    author = ... # a ForeignKey to settings.AUTH_USER_MODEL,  on delete cascade and related name to 'blog_posts'
    body = ... # a TextField
    publish = ... # a DateTimeField with default=timezone.now
    created = ... # a DateTimeField with auto_now_add=True
    updated = ... # a DateTimeField auto_now=True
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    post = ... # a ForeignKey to Post,  on delete cascade, and related name to 'comments'
    name = ... # a CharField with max_length=80
    email = ... # an EmailField
    body = ... # a TextField
    created = ... # a DateTimeField with auto_now_add=True
    updated = ... # a DateTimeField auto_now=True
    active = ... # a BooleanField with default=True

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
