from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_time', 'status')
    list_filter = ('status', 'author__username')
    search_fields = ('title', 'body', 'author__username')
    ordering = ('-status', 'published_time')
    date_hierarchy = 'published_time'
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
