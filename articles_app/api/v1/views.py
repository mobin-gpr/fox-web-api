from rest_framework.generics import ListAPIView, RetrieveAPIView
from articles_app.api.v1.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.network_services import get_ip

now = timezone.now()

# region - List Of Articles

class ArticleListAPIView(ListAPIView):
    queryset = ArticleModel.objects.filter(is_published=True, pub_date__lt=now).order_by('-pub_date')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
# endregion

# region - Detail of Articles

class ArticleDetailAPIView(RetrieveAPIView):
    queryset = ArticleModel.objects.filter(is_published=True, pub_date__lt=now).order_by('-pub_date')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        # If the visitor has not visited the article before, it records a visit for him/her
        user_ip = get_ip(request)
        if not ArticleVisitModel.objects.filter(article_id=instance.id, user=user_ip).exists():
            ArticleVisitModel.objects.create(article_id=instance.id, user=user_ip)

        return super().get(request, *args, **kwargs)

# endregion

# region - Handle The Article Likes & Dislikes Reactions

class ArticleReactionsAPIView(APIView):
    def post(self, request):
        serializer = ArticleReactionSerializer(data=request.data)

        if serializer.is_valid():
            # It takes the necessary values to record the user's reaction from the front-end developer
            article_id = serializer.validated_data.get('article_id')
            reaction = serializer.validated_data.get('reaction')
            user_ip = get_ip(request)

            # If the user clicks on the like button
            if reaction == 'like':

                # Checks if the user has already liked the article, does nothing (You can customize it to delete the previous like if the user had already liked the article)
                if ArticleLikesModel.objects.filter(user=user_ip, article_id=article_id).exists():
                    response = {
                        'like': ArticleLikesModel.objects.filter(article_id=article_id).count(),
                        'dislike': ArticleDisLikesModel.objects.filter(article_id=article_id).count()
                    }

                else:
                    # If the user had already disliked the article, it deletes it
                    if ArticleDisLikesModel.objects.filter(user=user_ip, article_id=article_id).exists():
                        ArticleDisLikesModel.objects.filter(user=user_ip, article_id=article_id).delete()

                    # Record a new like for article
                    ArticleLikesModel.objects.create(user=user_ip, article_id=article_id)
                    response = {
                        'like': ArticleLikesModel.objects.filter(article_id=article_id).count(),
                        'dislike': ArticleDisLikesModel.objects.filter(article_id=article_id).count()
                   }
            # If the user clicks on the dislike button
            elif reaction == 'dislike':
                # Checks if the user has already disliked the article, does nothing (You can customize it to delete the previous dislike if the user had already disliked the article)
                if ArticleDisLikesModel.objects.filter(user=user_ip, article_id=article_id).exists():
                    response = {
                        'like': ArticleLikesModel.objects.filter(article_id=article_id).count(),
                        'dislike': ArticleDisLikesModel.objects.filter(article_id=article_id).count()
                    }
                else:
                    # If the user had already liked the article, it deletes
                    if ArticleLikesModel.objects.filter(user=user_ip, article_id=article_id).exists():
                        ArticleLikesModel.objects.filter(user=user_ip, article_id=article_id).delete()

                    # Record a new dislike for article
                    ArticleDisLikesModel.objects.create(user=user_ip, article_id=article_id)
                    response = {
                        'like': ArticleLikesModel.objects.filter(article_id=article_id).count(),
                        'dislike': ArticleDisLikesModel.objects.filter(article_id=article_id).count()
                    }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion
