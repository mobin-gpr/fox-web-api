# Generated by Django 4.2 on 2024-05-17 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles_app", "0003_articlemodel_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articledislikesmodel",
            name="user",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="articlelikesmodel",
            name="user",
            field=models.CharField(max_length=100),
        ),
    ]
