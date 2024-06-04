import asyncio
import os
from os.path import join
from pathlib import Path
from dotenv import load_dotenv

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article, Subscriber
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from telegram import Bot
from asgiref.sync import sync_to_async

load_dotenv()

dotenv_path = join(Path(__file__).resolve().parent.parent, '.env')
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


async def notify_subscribers(article):
    """
    The notify_subscribers function is a coroutine that sends a message to all subscribers of the blog.
    It takes an article as its argument and uses it to construct the message.
    
    :param article: Pass the article object to the function
    :return: A coroutine object
    :doc-author: Trelent
    """
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    subscribers = await sync_to_async(list)(Subscriber.objects.all())
    message = f"New Article:\n\nTitle: {article.title}\n\n{article.content}"
    for subscriber in subscribers:
        print(subscriber.chat_id)
        await bot.send_message(chat_id=subscriber.chat_id, text=message)


class LatestArticleView(generics.ListAPIView):
    """
    The LatestArticleView class is a subclass of the ListAPIView class.
    It is used to retrieve the latest article from the database.
    """
    queryset = Article.objects.all().order_by('-published_date')[:1]
    serializer_class = ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    The ArticleViewSet class is a subclass of the ModelViewSet class.
    It is used to create, retrieve, update, and delete articles from the database.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        The perform_create function is called when a POST request is made to the ArticleList view.
        It creates an article object and saves it to the database, then calls notify_subscribers()
        to send out notifications.
        
        :param self: Represent the instance of the class
        :param serializer: Save the data to the database
        :return: The article object
        :doc-author: Trelent
        """
        article = serializer.save()
        print('created')
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(notify_subscribers(article))
        print('finished')


class SubscribeView(APIView):
    """
    The SubscribeView class is a subclass of the APIView class.
    It is used to allow users to subscribe to the bot.
    """
    def post(self, request, *args, **kwargs):
        """
        The post function allows a user to subscribe to the bot.
        
        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A response object
        :doc-author: Trelent
        """
        chat_id = request.data.get('chat_id')
        if Subscriber.objects.filter(chat_id=chat_id).exists():
            return Response({'status': 'Already subscribed'}, status=status.HTTP_200_OK)
        Subscriber.objects.create(chat_id=chat_id)
        return Response({'status': 'Subscribed'}, status=status.HTTP_201_CREATED)
