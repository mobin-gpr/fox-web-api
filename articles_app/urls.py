from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('reactions/', ArticleReactionsAPIView.as_view()),
    path('<slug:slug>/', ArticleDetailAPIView.as_view(), name='article-detail'),
]