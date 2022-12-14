from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import ListView
from taggit.models import Tag

from .models import Post, Comment
from .forms import CommentForm, SearchForm


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 12
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'


class PostTagListView(ListView):
    paginate_by = 6
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('slug')
        tag = Tag.objects.filter(
            slug=tag_slug
        )
        if tag.exists():
            context['tag'] = tag.first()
        else:
            context['tag'] = tag_slug
        return context

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        return Post.published.filter(
            tags__slug=tag_slug,
        )


def post_detail(request: WSGIRequest, slug: str):
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
    )
    print(post.related_posts.all())
    comments = post.comments.filter(
        active=True,
    )
    send_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment: Comment = form.save(commit=False)
            comment.post = post
            if comment.allow_to_send():
                comment.save()
            send_comment = True
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'send_comment': send_comment,
    }
    return render(request, 'blog/post/detail.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    context = {
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request, 'blog/post/search.html', context)
