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
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    subscribers = await sync_to_async(list)(Subscriber.objects.all())
    message = f"New Article:\n\nTitle: {article.title}\n\n{article.content}"
    for subscriber in subscribers:
        print(subscriber.chat_id)
        await bot.send_message(chat_id=subscriber.chat_id, text=message)


class LatestArticleView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-published_date')[:1]
    serializer_class = ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article = serializer.save()
        print('created')
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:  # There is no current event loop in the thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(notify_subscribers(article))
        print('finished')


class SubscribeView(APIView):
    def post(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id')
        if Subscriber.objects.filter(chat_id=chat_id).exists():
            return Response({'status': 'Already subscribed'}, status=status.HTTP_200_OK)
        Subscriber.objects.create(chat_id=chat_id)
        return Response({'status': 'Subscribed'}, status=status.HTTP_201_CREATED)
