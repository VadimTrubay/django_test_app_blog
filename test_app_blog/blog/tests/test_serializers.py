from django.test import TestCase
from test_app_blog.blog.models import Article, Subscriber
from test_app_blog.blog.serializers import ArticleSerializer, SubscriberSerializer


class ArticleSerializerTest(TestCase):

    def setUp(self):
        self.article_attributes = {
            'title': 'Test Article',
            'content': 'This is a test article.'
        }
        self.serializer_data = {
            'title': 'Test Article',
            'content': 'This is a test article.'
        }
        self.article = Article.objects.create(**self.article_attributes)
        self.serializer = ArticleSerializer(instance=self.article)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'content', 'published_date']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.article_attributes['title'])

    def test_content_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['content'], self.article_attributes['content'])


class SubscriberSerializerTest(TestCase):

    def setUp(self):
        self.subscriber_attributes = {
            'chat_id': '123456'
        }
        self.serializer_data = {
            'chat_id': '123456'
        }
        self.subscriber = Subscriber.objects.create(**self.subscriber_attributes)
        self.serializer = SubscriberSerializer(instance=self.subscriber)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['chat_id', 'created_at']))

    def test_chat_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['chat_id'], self.subscriber_attributes['chat_id'])
