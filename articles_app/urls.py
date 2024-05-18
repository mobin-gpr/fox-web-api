from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
    path('reactions/', ArticleReactionsAPIView.as_view()),
]