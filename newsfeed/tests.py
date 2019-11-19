from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory
from .views import NewsFeedViewSet, NewsPublisherViewSet, NewsKeywordViewSet
from .models import NewsPublisher, NewsFeed, Keyword
import json


class TestNews(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='a', password='secret')
        self.publisher = NewsPublisher.objects.create(name="BBC")
        self.news = NewsFeed.objects.create(title="News 1", content="123", publisher=self.publisher, link="abc")

    def test_get_without_login(self):
        factory = APIRequestFactory()
        view = NewsFeedViewSet.as_view({'get': 'list'})
        request = factory.get("/news/")
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['title'], "News 1")
        self.assertEqual(response.data['results'][0]['content'], "123")
        self.assertEqual(response.data['results'][0]['news_publisher']['name'], "BBC")

    def test_add_without_login(self):
        factory = APIRequestFactory()
        view = NewsFeedViewSet.as_view({'post': 'create'})
        request = factory.post("/news/", {"title": "News 2",
                                          "content": "abc",
                                          "news_publisher": self.publisher.id,
                                          "link": "abc"})
        response = view(request)
        self.assertTrue(response.status_code >= 400)

    def test_add_with_login(self):
        factory = APIRequestFactory()
        view = NewsFeedViewSet.as_view({'post': 'create'})
        request = factory.post("/news/", {"title": "News 2",
                                          "content": "abc",
                                          "publisher": self.publisher.id,
                                          "link": "abcd"}, format="json")

        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], "News 2")
        self.assertEqual(response.data['content'], "abc")
        self.assertEqual(response.data['news_publisher']['name'], "BBC")


class TestKeyword(APITestCase):
    def setUp(self):
        self.publisher = NewsPublisher.objects.create(name="BBC")
        self.news = NewsFeed.objects.create(title="News 1", content="123", publisher=self.publisher, link="abc")

    def test_add_keyword(self):
        factory = APIRequestFactory()
        view = NewsKeywordViewSet.as_view({'post': 'create'})
        request = factory.post("/keyword/", {
            "feed": self.news.id,
            "keyword": "test"
        })
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['keyword'], "test")

    def test_add_multiple_keyword(self):
        factory = APIRequestFactory()
        view = NewsKeywordViewSet.as_view({'post': 'create'})
        request = factory.post("/keyword/", json.dumps([{
            "feed": self.news.id,
            "keyword": "test"
        }, {
            "feed": self.news.id,
            "keyword": "test 2"
        }]), content_type="application/json")
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data[0]), 2)
        self.assertEqual(response.data[0]['keyword'], 'test')
        self.assertEqual(response.data[1]['keyword'], 'test 2')

    def test_add_dup_keyword(self):
        """
        When adding the same keyword to the database,
        it won't do so. One unique keyword per feed
        :return:
        """
        factory = APIRequestFactory()
        view = NewsKeywordViewSet.as_view({'post': 'create'})
        factory.post("/keyword/", {
            "feed": self.news.id,
            "keyword": "test"
        })
        request = factory.post("/keyword/", {
            "feed": self.news.id,
            "keyword": "test"
        })
        response = view(request)
        data = Keyword.objects.all()
        self.assertEqual(len(data), 1)
