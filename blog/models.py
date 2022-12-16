from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status='published',
        )


class PostManager(models.Manager):
    def with_documents(self):
        vector = SearchVector('title', weight='A') + \
            SearchVector('body', weight='B')
        return self.get_queryset().annotate(document=vector)


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        PUBLISHED = "published"

    title = models.CharField(
        max_length=128,
    )
    slug = models.CharField(
        max_length=128,
        unique=True,
    )
    description = models.CharField(
        max_length=256,
    )
    body = RichTextUploadingField()
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
    related_posts = models.ManyToManyField(
        'self',
        blank=True,
    )
    search_vector = SearchVectorField(
        null=True,
        blank=True,
    )

    objects = PostManager()
    published = PublishManager()

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=(self.slug,)
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        change_search_vector = "update_fields" not in kwargs \
            or "search_vector" not in kwargs["update_fields"]
        if change_search_vector:
            instance: Post = self._meta.default_manager\
                .with_documents().get(pk=self.pk)
            instance.search_vector = instance.document
            instance.save(update_fields=["search_vector"])

    def __str__(self):
        return self.title

    class Meta:
        ordering = (
            '-published_at',
        )
        indexes = [
            GinIndex(
                fields=["search_vector"],
                name="title_body_index",
            ),
        ]


@receiver(post_save, sender=Post)
@on_transaction_commit
def set_related_posts(instance: Post, **kwargs):
    tags = instance.tags.values_list(
        'id',
        flat=True,
    )
    related_posts = (
        Post.published
        .filter(tags__in=tags)
        .distinct()
        .exclude(id=instance.id)
        .annotate(same_tags=Count('tags'))
        .order_by('-same_tags', '-published_at')
        .values_list('id', flat=True)[:4]
    )
    instance.related_posts.clear()
    instance.related_posts.add(*related_posts)


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
