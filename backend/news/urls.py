from django.urls import path
from .views import NewsListCreateView, MyNewsListView, NewsDetailView, CommentListCreateView, SavedNewsView

urlpatterns = [
    path("news/", NewsListCreateView.as_view(), name="news-list-create"),
    path("my-news/", MyNewsListView.as_view(), name="my-news"),
    path("news/<int:news_id>/", NewsDetailView.as_view(), name="news-detail"),
    path("comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("saved-news/", SavedNewsView.as_view(), name="saved-news"),
]
