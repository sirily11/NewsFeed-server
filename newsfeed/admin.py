from django.contrib import admin
from .models import NewsFeed, NewsPublisher, Keyword

# Register your models here.
admin.site.register(NewsFeed)
admin.site.register(NewsPublisher)
admin.site.register(Keyword)