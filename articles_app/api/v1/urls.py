from django.urls import path
from articles_app.api.v1.views import *

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('reactions/', ArticleReactionsAPIView.as_view()),
    path('detail/<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
]