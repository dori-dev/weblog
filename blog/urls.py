from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path(
        '<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'tag/<slug:slug>/',
        views.PostTagListView.as_view(),
        name='post_list_by_tag'
    ),
]
