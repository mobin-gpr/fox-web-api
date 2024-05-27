from django.urls import path
from articles_app.api.v1.views import *

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('post/reactions/', ArticleReactionsAPIView.as_view()),
    path('<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('<slug:slug>/reactions/', ArticleReactionsAPIView.as_view()),
    path('tags/all/', TagsListAPIView.as_view()),
]