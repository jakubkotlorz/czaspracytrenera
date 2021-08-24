from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created', 'updated', 'lead_image', 'status']
    list_filter = ['publish', 'status']
