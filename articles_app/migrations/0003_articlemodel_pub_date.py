# Generated by Django 4.2 on 2024-05-17 16:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (
            "articles_app",
            "0002_alter_articlemodel_image_articlevisitmodel_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="articlemodel",
            name="pub_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
