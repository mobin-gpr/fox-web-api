from django.core.management.base import BaseCommand
from faker import Faker
from users_app.models import User
from articles_app.models import (
    ArticleModel,
    TagModel,
    ArticleVisitModel,
    ArticleLikesModel,
    ArticleDisLikesModel,
)
import random
from django.utils import timezone


class Command(BaseCommand):
    """Create fake data for testing"""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()
        self.user_counts = 40
        self.tag_counts = 30
        self.article_counts = 100
        self.min_view_counts = 1
        self.max_view_counts = 50
        self.min_like_counts = 5
        self.max_like_counts = 50
        self.min_dislike_counts = 5
        self.max_dislike_counts = 50
        self.task_counts = 3

    def handle(self, *args, **options):
        print("------------------------------")
        print("This can take a while...")
        try:
            # Create users
            print("------------------------------")
            print(f"Creating fake data for users...[1/{self.task_counts}]")
            for _ in range(40):
                User.objects.create_user(
                    email=self.faker.email(),
                    password="Test@123",
                    is_active=True,
                    is_verified=True,
                    first_name=self.faker.first_name(),
                    last_name=self.faker.last_name(),
                )

            # Create tags
            print("------------------------------")
            print(f"Creating fake data for tags...[2/{self.task_counts}]")
            for _ in range(30):
                TagModel.objects.create(
                    name=self.faker.word(), slug=self.faker.slug(), is_active=True
                )

            # Create articles
            print("------------------------------")
            print(
                f"Creating fake data for articles, views, likes & dislikes...[3/{self.task_counts}]"
            )
            tag_list = []
            tag_count = TagModel.objects.count()
            for _ in range(5):
                random_tag = random.randint(1, tag_count - 1)
                tag = TagModel.objects.all()[random_tag]
                tag_list.append(tag.slug)
            author_count = User.objects.count()
            random_author = random.randint(1, author_count - 1)
            author = User.objects.all()[random_author]

            for _ in range(100):
                article = ArticleModel.objects.create(
                    author=author,
                    title=self.faker.word(),
                    meta_description=self.faker.paragraph(nb_sentences=1),
                    content=self.faker.paragraph(nb_sentences=40),
                    slug=self.faker.slug(),
                    pub_date=timezone.now(),
                    is_published=random.choice([True, False]),
                )
                for slug in tag_list:
                    tag = TagModel.objects.get(slug=slug)
                    article.tags.add(tag)
                    article.save()

                    # Create view for article
                    for _ in range(
                        random.randint(self.min_view_counts, self.max_view_counts)
                    ):
                        ArticleVisitModel.objects.create(
                            article=article, user=self.faker.ipv4()
                        )

                    # Create like for article
                    for _ in range(
                        random.randint(self.min_like_counts, self.max_like_counts)
                    ):
                        ArticleLikesModel.objects.create(
                            article=article, user=self.faker.ipv4()
                        )

                    # Create dislike for article
                    for _ in range(
                        random.randint(self.min_dislike_counts, self.max_dislike_counts)
                    ):
                        ArticleDisLikesModel.objects.create(
                            article=article, user=self.faker.ipv4()
                        )
        except:
            pass
        print("------------------------------")
        print("All done!")
