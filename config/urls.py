"""Weblog URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap, StaticViewSitemap

sitemaps = {
    'statics': StaticViewSitemap,
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path(
        'sitemap.xml', sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]
