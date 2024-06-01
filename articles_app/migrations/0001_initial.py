# Generated by Django 4.2 on 2024-05-17 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TagModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=400, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="ArticleModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "seo_description",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("content", django_ckeditor_5.fields.CKEditor5Field()),
                ("slug", models.SlugField(max_length=400, unique=True)),
                ("image", models.ImageField(upload_to="images/news/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_published", models.BooleanField(default=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tag", models.ManyToManyField(to="articles_app.tagmodel")),
            ],
        ),
    ]
