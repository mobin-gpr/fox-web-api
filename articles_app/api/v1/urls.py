from django.urls import path
from articles_app.api.v1.views import *

urlpatterns = [
    path("", ArticleListAPIView.as_view()),  # Articles lists
    path(
        "action/reactions/", ArticleReactionsAPIView.as_view()
    ),  # Handle article reactions (like & dislike)
    path(
        "<slug:slug>/", ArticleDetailAPIView.as_view(), name="article-detail"
    ),  # Article detail (single article)
    path("tags/all/", TagsListAPIView.as_view()),  # Tags lists
]
