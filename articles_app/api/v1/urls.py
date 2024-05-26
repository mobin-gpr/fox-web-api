from django.urls import path
from articles_app.api.v1.views import *

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('reactions/', ArticleReactionsAPIView.as_view()),
    path('detail/<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('tag/<slug:slug>/', FilterArticleByTagAPIView.as_view(), name='filter-article-by-tags'),
    path('author/<str:username>/', FilterArticleByAuthorAPIView.as_view(), name='filter-article-by-author'),
]