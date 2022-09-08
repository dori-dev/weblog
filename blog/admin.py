from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author',
        'published_time',
        'status',
    )
    list_filter = (
        'status',
        'author__username',
    )
    search_fields = (
        'title',
        'body',
        'author__username',
    )
    date_hierarchy = 'published_time'
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }
    raw_id_fields = (
        'author',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'post',
        'email',
        'created',
        'active',
    )
    list_filter = (
        'active',
        'post',
    )
    search_fields = (
        'name',
        'email',
        'body',
    )
    date_hierarchy = 'updated'
    raw_id_fields = (
        'post',
    )
