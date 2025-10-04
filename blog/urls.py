from django.urls import path

from . import views
from .feeds import LatestPostsFeed


app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("tag/<slug:tag_slug>/", views.PostListView.as_view(), name="post-list-by-tag"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post-detail"),
    path("<int:post_id>/share/", views.EmailPostView.as_view(), name="post-share"),
    path("<int:post_id>/comment/", views.CommentView.as_view(), name="post-comment"),
    path("feed/", LatestPostsFeed(), name="post-feed"),
    path("search/", views.post_search, name="post-search"),
]
