from django.db import models
from django.db.models.fields import TextField


class Search(models.Lookup):
    lookup_name = 'fts'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN natural language mode)' % (lhs, rhs), params


# Create your models here.
class NewsPublisher(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class NewsFeed(models.Model):
    title = models.CharField(unique=True, max_length=128)
    link = models.CharField(max_length=255, unique=True)
    cover = models.CharField(null=True, blank=True, max_length=1024)
    publisher = models.ForeignKey(NewsPublisher, on_delete=models.SET_NULL, null=True)
    # noinspection PyCallingNonCallable
    content = models.TextField(null=True, blank=True)
    # noinspection PyCallingNonCallable
    posted_time = models.DateTimeField(auto_now_add=True)
    # noinspection PyCallingNonCallable
    sentiment = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title


class Keyword(models.Model):
    keyword = models.CharField(max_length=128)
    feed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE, related_name="keywords")

    def __str__(self):
        return self.keyword

    class Meta:
        unique_together = ("feed", "keyword")

# Comment following lines if you use sqlite
# TextField.register_lookup(Search)
