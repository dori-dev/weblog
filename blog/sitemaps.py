from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post


class StaticViewSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return [
            'blog:post_list',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        newest_post: Post = Post.published.first()
        return newest_post.updated_at


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Post.published.all()

    def lastmod(self, obj: Post):
        return obj.updated_at
