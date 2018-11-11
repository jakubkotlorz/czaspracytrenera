from django.urls import path

from . import views

app_name = 'managers'
urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:country_id>/', views.country, name='country'),
    path('t/<int:club_id>/', views.club, name='club'),
    path('m/<int:manager_id>/', views.profile, name='profile'),
    path('cup/<int:cup_id>/', views.season, name='season'),
    path('news/', views.news, name='news'),
    path('managers/', views.managers, name='managers'),
]