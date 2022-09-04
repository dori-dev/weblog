from django.views.generic import DetailView, ListView
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 1
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    queryset = Post.published.all()
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'
