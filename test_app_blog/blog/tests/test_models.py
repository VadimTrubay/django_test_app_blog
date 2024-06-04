from django.test import TestCase
from test_app_blog.blog.models import Article, Subscriber


class ArticleModelTest(TestCase):

    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article."
        )

    def test_article_creation(self):
        self.assertIsInstance(self.article, Article)
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.content, "This is a test article.")


class SubscriberModelTest(TestCase):

    def setUp(self):
        self.subscriber = Subscriber.objects.create(chat_id="123456")

    def test_subscriber_creation(self):
        self.assertIsInstance(self.subscriber, Subscriber)
        self.assertEqual(self.subscriber.chat_id, "123456")
