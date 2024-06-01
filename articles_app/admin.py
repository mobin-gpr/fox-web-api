from django.contrib import admin
from .models import (
    ArticleModel,
    TagModel,
    ArticleVisitModel,
    ArticleLikesModel,
    ArticleDisLikesModel,
)


@admin.register(ArticleModel)
class ArticleModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TagModel)
class TagModel(admin.ModelAdmin):
    pass


@admin.register(ArticleVisitModel)
class ArticleVisitModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleLikesModel)
class ArticleLikesModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleDisLikesModel)
class ArticleDisLikesModelAdmin(admin.ModelAdmin):
    pass
