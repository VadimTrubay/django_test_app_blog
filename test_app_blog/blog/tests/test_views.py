from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from test_app_blog.blog.models import Article, Subscriber
from test_app_blog.blog.serializers import ArticleSerializer


class ArticleViewSetTest(APITestCase):

    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article."
        )
        self.url = reverse('article-list')

    def test_get_articles(self):
        response = self.client.get(self.url)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class SubscribeViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('subscribe')

    def test_subscribe(self):
        data = {'chat_id': '123456'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertEqual(Subscriber.objects.get().chat_id, '123456')

    def test_already_subscribed(self):
        Subscriber.objects.create(chat_id='123456')
        data = {'chat_id': '123456'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Already subscribed')
