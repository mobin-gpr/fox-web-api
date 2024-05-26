from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model

User = get_user_model()

# region - Model Of Article tag

class TagModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=400, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# endregion

# region - Model Of Article

class ArticleModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=200, null=True, blank=True)
    # content = CKEditor5Field(config_name='extends')
    content = models.TextField()
    slug = models.SlugField(max_length=400, unique=True)
    image = models.ImageField(upload_to='images/articles/')
    tags = models.ManyToManyField(TagModel)
    created_at = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# endregion


# region - Model Of Article Visits

class ArticleVisitModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.article.title + self.user

# endregion

# region - Model Of Article Likes

class ArticleLikesModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.article.title + self.user

# endregion

# region - Model Of Article Dislikes

class ArticleDisLikesModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.article.title + self.user

# endregion
