from django.urls import path

from . import views

app_name = 'managers'
urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:country_id>/', views.country, name='country'),
    path('m/<int:manager_id>/', views.profile, name='profile'),
]