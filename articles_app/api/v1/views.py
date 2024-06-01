from rest_framework.generics import ListAPIView, RetrieveAPIView
from articles_app.api.v1.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.network_services import get_ip
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ...paginattion import DefaultPagination

now = timezone.now()


# region - List Of Articles


class ArticleListAPIView(ListAPIView):
    """
    This view is for getting all articles
    """

    queryset = ArticleModel.objects.filter(
        is_published=True, pub_date__lte=now
    ).order_by("-pub_date")
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"tags": ["exact", "in"], "author": ["exact", "in"]}
    search_fields = ["title", "content"]
    ordering_fields = ["pub_date", "created_at"]
    pagination_class = DefaultPagination


# endregion

# region - Detail of Articles


class ArticleDetailAPIView(RetrieveAPIView):
    """
    This view is for getting a single article
    """

    queryset = ArticleModel.objects.filter(
        is_published=True, pub_date__lte=now
    ).order_by("-pub_date")
    serializer_class = ArticleSerializer
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # If the visitor has not visited the article before, it records a visit for him/her
        user_ip = get_ip(request)
        if not ArticleVisitModel.objects.filter(
            article_id=instance.id, user=user_ip
        ).exists():
            ArticleVisitModel.objects.create(article_id=instance.id, user=user_ip)

        return super().get(request, *args, **kwargs)


# endregion

# region - Handle The Article Likes & Dislikes Reactions


class ArticleReactionsAPIView(APIView):
    """
    This view is for handling articles reactions
    """

    serializer_class = ArticleReactionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # It takes the necessary values to record the user's reaction from the front-end developer
            article_id = serializer.validated_data.get("article_id")
            reaction = serializer.validated_data.get("reaction")
            user_ip = get_ip(request)

            # Checks if article exists
            if ArticleModel.objects.filter(id=article_id).exists():
                # If the user clicks on the like button
                if reaction == "like":

                    # Checks if the user has already liked the article, does nothing (You can customize it to delete the previous like if the user had already liked the article)
                    if ArticleLikesModel.objects.filter(
                        user=user_ip, article_id=article_id
                    ).exists():
                        response = {
                            "like": ArticleLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                            "dislike": ArticleDisLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                        }

                    else:
                        # If the user had already disliked the article, it deletes it
                        if ArticleDisLikesModel.objects.filter(
                            user=user_ip, article_id=article_id
                        ).exists():
                            ArticleDisLikesModel.objects.filter(
                                user=user_ip, article_id=article_id
                            ).delete()

                        # Record a new like for article
                        ArticleLikesModel.objects.create(
                            user=user_ip, article_id=article_id
                        )
                        response = {
                            "like": ArticleLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                            "dislike": ArticleDisLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                        }
                # If the user clicks on the dislike button
                elif reaction == "dislike":
                    # Checks if the user has already disliked the article, does nothing (You can customize it to delete the previous dislike if the user had already disliked the article)
                    if ArticleDisLikesModel.objects.filter(
                        user=user_ip, article_id=article_id
                    ).exists():
                        response = {
                            "like": ArticleLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                            "dislike": ArticleDisLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                        }
                    else:
                        # If the user had already liked the article, it deletes
                        if ArticleLikesModel.objects.filter(
                            user=user_ip, article_id=article_id
                        ).exists():
                            ArticleLikesModel.objects.filter(
                                user=user_ip, article_id=article_id
                            ).delete()

                        # Record a new dislike for article
                        ArticleDisLikesModel.objects.create(
                            user=user_ip, article_id=article_id
                        )
                        response = {
                            "like": ArticleLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                            "dislike": ArticleDisLikesModel.objects.filter(
                                article_id=article_id
                            ).count(),
                        }

                return Response(response, status=status.HTTP_200_OK)

            # Checks if article not exists return 404
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# endregion


class TagsListAPIView(ListAPIView):
    """
    This view is for getting all tags
    """

    queryset = TagModel.objects.filter(is_active=True)
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"name": ["exact", "in"]}
    search_fields = ["name"]
    pagination_class = DefaultPagination
