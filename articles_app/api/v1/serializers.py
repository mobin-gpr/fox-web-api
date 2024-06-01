from rest_framework import serializers
from articles_app.models import (
    ArticleModel,
    TagModel,
    ArticleLikesModel,
    ArticleDisLikesModel,
    ArticleVisitModel,
)
from users_app.models import User
from utils.text_editor import snippet


# region - Serializer Of Authors


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


# endregion


# region - Serializer Of Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ["id", "name", "slug"]

        # endregion

        # region - Serializer Of Article


class ArticleSerializer(serializers.ModelSerializer):
    reactions = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    content_summary = serializers.SerializerMethodField()

    class Meta:
        model = ArticleModel
        fields = [
            "id",
            "title",
            "author",
            "tags",
            "meta_description",
            "content",
            "content_summary",
            "slug",
            "image",
            "reactions",
            "views",
            "url",
            "created_at",
            "pub_date",
        ]

    def to_representation(self, instance):
        """
        Separating the display mode of the fields from the manipulation mode of the fields
        """
        rep = super().to_representation(instance)
        request = self.context.get("request")

        # Separation of fields in the list and details page
        if request.parser_context["kwargs"].get("slug"):
            rep.pop("url")
            rep.pop("content_summary")
            rep.pop("slug")
        else:
            rep.pop("content")

        # tags
        tags = TagSerializer(
            instance.tags.filter(is_active=True),
            many=True,
            context={"request": request},
        ).data
        custom_tags = []
        for tag in tags:
            tag.pop("slug", None)
            custom_tags.append(tag)
        rep["tags"] = custom_tags

        # author
        author = AuthorSerializer(
            instance.author, many=False, context={"request": request}
        ).data
        rep["author"] = author

        return rep

    def get_url(self, obj):
        """
        return articles absolute url
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

    def get_reactions(self, obj):
        """
        Returns the number of likes and dislikes of the article
        """
        likes_count = ArticleLikesModel.objects.filter(article_id=obj.id).count()
        likes = likes_count if not None else 0
        dislikes_count = ArticleDisLikesModel.objects.filter(article_id=obj.id).count()
        dislikes = dislikes_count if not None else 0
        reactions = {"likes": likes, "dislikes": dislikes}
        return reactions

    def get_views(self, obj):
        """
        Returns the number of article views
        """
        view_count = ArticleVisitModel.objects.filter(article_id=obj.id).count()
        return view_count

    def get_content_summary(self, obj):
        """
        Returns the content summary of the article
        """
        summary = snippet(obj.content, 20)
        return summary


# endregion

# region - Serializer Of Article Reactions (Like & Dislikes)


class ArticleReactionSerializer(serializers.Serializer):
    article_id = serializers.CharField(max_length=20)
    reaction = serializers.CharField(max_length=20)


# endregion
