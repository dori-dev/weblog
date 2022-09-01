from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from .models import Post


def post_list(request: WSGIRequest):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request: WSGIRequest, slug: str):
    post = get_object_or_404(Post, slug=slug, status='published')
    context = {
        'post': post
    }
    return render(request, 'blog/post/detail.html', context)
