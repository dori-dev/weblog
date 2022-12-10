from datetime import datetime
from ..models import Post
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag(
    name='posts_count',
)
def total_posts():
    return Post.published.count()


@register.inclusion_tag(
    'blog/post/latest_posts.html',
    name='latest_posts',
)
def show_latest_posts(count: int = 5):
    latest_posts = Post.published.all()[:count]
    return {
        'latest_posts': latest_posts,
    }


@register.inclusion_tag(
    'blog/post/most_commented_posts.html',
    name='most_commented_posts',
)
def get_most_commented_posts(count: int = 3):
    most_commented_posts = Post.published.annotate(
        total_comments=Count('comments')
    ).order_by(
        '-total_comments',
        '-published_at',
    )[:count]
    return {
        'most_commented_posts': most_commented_posts,
    }


@register.filter('formatted')
def change_datetime_format(value: datetime, format: str = None):
    if format is None:
        format = '%B %d, %I:%M %p'
    return value.strftime(format)
