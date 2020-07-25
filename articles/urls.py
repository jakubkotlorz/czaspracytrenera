from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ArticleFullView

app_name = 'articles'
urlpatterns = [
    path('<slug:slug>/', ArticleFullView.as_view(), name='article')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
