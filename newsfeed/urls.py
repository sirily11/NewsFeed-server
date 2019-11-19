from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsFeedViewSet, base_name="news")
router.register(r"publisher", views.NewsPublisherViewSet, base_name="publisher")
router.register(r"keyword", views.NewsKeywordViewSet, base_name="keyword")

urlpatterns = [
    path('', include(router.urls)),
    path('redirect', views.NewsRedirectView.as_view())
]
