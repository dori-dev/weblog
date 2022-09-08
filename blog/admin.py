from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author',
        'published_at',
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
    date_hierarchy = 'published_at'
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
        'created_at',
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
    date_hierarchy = 'updated_at'
    raw_id_fields = (
        'post',
    )
