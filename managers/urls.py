from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('country/<int:country_id>/', views.country, name='country'),
    path('<int:manager_id>/', views.profile, name='profile'),
]