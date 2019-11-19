from django.contrib.auth.models import User
from rest_framework import serializers
from .models import NewsPublisher, NewsFeed, Keyword


class NewsPublisherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsPublisher
        fields = ("id", "name",)


class NewsKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ("feed", "keyword")


class NewsFeedSerializer(serializers.ModelSerializer):
    news_publisher = NewsPublisherSerializer(source="publisher", read_only=True)
    keywords = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = NewsFeed
        fields = (
            "id", "title", "link", "cover", "news_publisher", "content", "sentiment", "posted_time", "publisher",
            "keywords")
