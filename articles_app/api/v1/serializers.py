from rest_framework import serializers
from articles_app.models import *
from django.urls import reverse


# region - Serializer Of Article
class ArticleSerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = ArticleModel
        fields = '__all__'

    def get_url(self, obj):
        """
        return articles absolute url
        """
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())

    def get_reactions(self, obj):
        """
        Returns the number of likes and dislikes of the article
        """
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
        """
        Returns the number of article views
        """
        view_count = ArticleVisitModel.objects.filter(article_id=obj.id).count()
        return view_count

    def get_tags(self, obj):
        """
        Override the value of tags to return more useful information instead of ID
        """
        ################### FORMAT ONE ###################

        # tags = {}
        # filter_tags = obj.tags.filter(is_active=True)
        # for i, tag in enumerate(filter_tags, start=1):
        #     tags[i] = {}
        #     tags[i]['name'] = tag.name
        #     tags[i]['url'] = reverse('filter-article-by-tags', kwargs={'slug': tag.slug})
        # return tags

        ################### END FORMAT ONE ###################


        ################### FORMAT TWO ###################
        request = self.context.get('request')
        tags = []
        filter_tags = obj.tags.filter(is_active=True)
        for tag in filter_tags:
            values = {
                'name': tag.name,
                'url': request.build_absolute_uri(tag.get_absolute_url()),
            }
            tags.append(values)
        return tags

        ################### END FORMAT TWO ###################
    def get_author(self, obj):
        """
        Override the value of author to return more useful information instead of ID
        """
        request = self.context.get('request')
        author = {}
        # Checks if the author has set the first name and last name, returns it in the author's profile
        if full_name:=obj.author.get_full_name():
            author['full_name'] = full_name
        username = obj.author.username
        author['username'] = username
        author['url'] = request.build_absolute_uri(reverse('filter-article-by-author', kwargs={'username': username}))
        return author

# endregion

# region - Serializer Of Article Reactions (Like & Dislikes)

class ArticleReactionSerializer(serializers.Serializer):
    article_id = serializers.CharField(max_length=20)
    reaction = serializers.CharField(max_length=20)

# endregion
