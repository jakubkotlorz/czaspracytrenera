from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
                .filter(status='published') \
                .order_by('-created') \


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    header_desc = models.TextField(max_length=250, null=True, blank=True)
    header_keys = models.TextField(max_length=250, null=True, blank=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'articles')
    lead_image = models.ImageField(upload_to='articles-images/%Y/')
    intro = models.TextField(null=True, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default = 'draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('articles:article', args=[str(self.slug)])

    def __str__(self):
        return self.title
