from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'The Weblog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of the weblog.'

    def items(self):
        return Post.published.all()[:16]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post):
        return truncatewords(item.body, 32)
