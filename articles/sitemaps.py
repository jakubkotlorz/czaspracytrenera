from django.contrib.sitemaps import Sitemap
from articles.models import Article

class ArticlesSitemap(Sitemap):

    def items(self):
        return Article.published.all()
