from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.core.handlers.wsgi import WSGIRequest
from .models import Post


def post_list(request: WSGIRequest):
    post_objects = Post.published.all()
    paginator = Paginator(post_objects, 12)
    page = request.GET.get('page')
    if page is None or not page.isdigit():
        page = 1
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
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
