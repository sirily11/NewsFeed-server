from rest_framework import viewsets
from .serializers import NewsPublisherSerializer, NewsFeedSerializer, NewsKeywordSerializer
from .models import NewsFeed, NewsPublisher, Keyword
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response


class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all().order_by("-posted_time")
    serializer_class = NewsFeedSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['publisher']
    search_fields = ["content", "title"] # comment this line if you use mysql
    pagination_class = LimitOffsetPagination

    # Comment following lines if you use sqlite
    # def get_queryset(self):
    #     queryset = NewsFeed.objects.all().order_by("-posted_time")
    #     search = self.request.query_params.get("search")
    #     if search:
    #         queryset = NewsFeed.objects.filter(content__fts=search).order_by("-posted_time")
    #
    #     return queryset


class NewsPublisherViewSet(viewsets.ModelViewSet):
    queryset = NewsPublisher.objects.all()
    serializer_class = NewsPublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsKeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = NewsKeywordSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(NewsKeywordViewSet, self).get_serializer(*args, **kwargs)


class NewsRedirectView(APIView):
    def get(self, request, format=None):
        link = request.query_params.get("link")
        if link:
            obj = NewsFeed.objects.filter(link=link).first()
            serializer = NewsFeedSerializer(obj)
            if obj:
                return Response(data=serializer.data)
        return Response(data={"error": "No link"}, status=400)
