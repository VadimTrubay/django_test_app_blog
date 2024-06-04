from rest_framework import serializers
from .models import Article, Subscriber


class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for the Article model. """
    class Meta:
        model = Article
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    """ Serializer for the Subscriber model. """
    class Meta:
        model = Subscriber
        fields = ['chat_id', 'created_at']
