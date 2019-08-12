from django.urls import path

from . import views

app_name = 'managers'
urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:country_id>/', views.country, name='country'),
    path('team/<slug:slug>/', views.club, name='team'),
    path('manager/<slug:slug>/', views.profile, name='profile'),
    path('season/add/', views.SeasonCreateView.as_view(), name='season-add'),
    path('season/<slug:slug>/update', views.SeasonUpdateView.as_view(), name='season-update'),
    path('season/<slug:slug>/', views.season, name='season'),
    path('seasons/list', views.SeasonListView.as_view(), name='season-list'),
    path('news/', views.news, name='news'),
    path('managers/', views.managers, name='managers'),
    path('search/', views.search, name='search'),
]