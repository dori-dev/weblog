from ..models import Post
from django import template

register = template.Library()


@register.simple_tag(name='posts_count')
def total_posts():
    return Post.published.count()


@register.inclusion_tag(
    'blog/post/latest_posts.html',
    name='latest_posts')
def show_latest_posts(count: int = 5):
    latest_posts = Post.published.all()[:count]
    return {
        'latest_posts': latest_posts,
    }
