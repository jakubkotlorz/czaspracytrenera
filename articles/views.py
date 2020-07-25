from django.views.generic.detail import DetailView

from .models import Article

class ArticleFullView(DetailView):

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    