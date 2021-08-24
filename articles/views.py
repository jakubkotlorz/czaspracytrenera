from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article

class ArticleFullView(DetailView):

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.published.all()
        return context


class ArticleListView(ListView):

    model = Article
    queryset = Article.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context