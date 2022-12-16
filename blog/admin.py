from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post, Comment


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
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
