from django.urls import path

from . import views

app_name = 'managers'
urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:country_id>/', views.country, name='country'),
    path('team/<slug:slug>/', views.club, name='team'),
    path('manager/<slug:slug>/', views.profile, name='profile'),
    path('season/<slug:slug>/', views.season, name='season'),
    path('news/', views.news, name='news'),
    path('managers/', views.managers, name='managers'),
    path('search/', views.search, name='search'),
]