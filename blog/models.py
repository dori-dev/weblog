from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='published',
        )


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            active=True,
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        PUBLISHED = "published"

    title = models.CharField(
        max_length=256,
    )
    slug = models.CharField(
        max_length=256,
        unique=True,
    )
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
    )
    updated_time = models.DateTimeField(
        auto_now=True,
    )
    published_time = models.DateTimeField(
        default=timezone.now,
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default='draft',
    )
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=(self.slug,)
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-published_time',
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(
        max_length=64,
    )
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    active = models.BooleanField(
        default=True,
    )
    objects = models.Manager()
    actives = ActiveManager()

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'

    class Meta:
        ordering = (
            'created',
        )
