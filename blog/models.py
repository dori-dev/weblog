from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='published',
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
        related_name='posts',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    published_at = models.DateTimeField(
        default=timezone.now,
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default='draft',
    )
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishManager()

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=(self.slug,)
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-published_at',
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
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    active = models.BooleanField(
        default=True,
    )

    def allow_to_send(self,):
        exists = Comment.objects.filter(
            post=self.post,
            email=self.email,
        ).exists()
        if exists:
            return False
        return True

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'

    class Meta:
        ordering = (
            'created_at',
        )
