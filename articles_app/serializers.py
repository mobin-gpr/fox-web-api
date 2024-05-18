from rest_framework import serializers
from .models import *
from django.urls import reverse


# region - Serializer Of Article
class ArticleSerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    class Meta:
        model = ArticleModel
        fields = '__all__'

    def get_url(self, obj):
        return reverse('article-detail', kwargs={'slug': obj.slug})
    def get_reactions(self, obj):
        likes_count = ArticleLikesModel.objects.filter(article_id=obj.id).count()
        likes = likes_count if not None else 0
        dislikes_count = ArticleDisLikesModel.objects.filter(article_id=obj.id).count()
        dislikes = dislikes_count if not None else 0
        reactions = {
            'likes': likes,
            'dislikes': dislikes
        }
        return reactions

    def get_views(self, obj):
        view_count = ArticleVisitModel.objects.filter(article_id=obj.id).count()
        return view_count

# endregion

# region - Serializer Of Article Reactions (Like & Dislikes)

class ArticleReactionSerializer(serializers.Serializer):
    article_id = serializers.CharField(max_length=20)
    reaction = serializers.CharField(max_length=20)

# endregion