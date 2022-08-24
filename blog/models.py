from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        PUBLISHED = "published"

    title = models.CharField(
        max_length=256,
    )
    slug = models.CharField(
        max_length=256,
        unique_for_date='published',
    )
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    published = models.DateTimeField(
        default=timezone.now,
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default='draft',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-published',
        )
