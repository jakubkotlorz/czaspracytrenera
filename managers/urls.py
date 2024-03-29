from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'managers'
urlpatterns = [
    # for moderators only
    path('logout', views.logout_view, name='logout-page'),

    path('ajax/get_season_list', views.get_list_seasons, name='ajax-get-season-list'),

    path('season_menu_list', views.season_menu_list, name='season-menu-list'),
    path('season_menu_list/add/<int:season_id>/', views.season_menu_list_add, name='season-menu-list-add'),
    path('season_menu_list/<int:season_id>/<str:action>', views.season_menu_list_change, name='season-menu-list-edit'),

    path('job/add/', views.AddJobView.as_view(), name='add-job'),
    path('job/<int:pk>/end/', views.EndJobView.as_view(), name='end-job'),
    path('team/<slug:slug>/add-job/', views.TeamAddJobView.as_view(), name='team-add-job'),
    path('manager/add/', views.PersonAddView.as_view(), name='person-add'),
    path('manager/<slug:slug>/update-photo', views.profile_photo_view, name='profile-update-photo'),
    path('manager/<slug:slug>/update-personal', views.PersonalDataProfileView.as_view(), name='profile-update-personal'),
    path('manager/<slug:slug>/add-managerial-history', views.add_managerial_history_view, name='profile-add-managerial-history'),
    path('season/<slug:slug>/update', views.SeasonUpdateView.as_view(), name='season-update'),
    path('season/add/', views.SeasonCreateView.as_view(), name='season-add'),
    path('season/<slug:slug>/avance', views.season_avance, name='season-avance'),
    path('season/<slug:slug>/delete', views.SeasonDeleteView.as_view(), name='season-delete'), 
    path('season/<slug:slug>/set_current', views.season_set_current, name='season-set-current'),

    path('managers/', views.managers, name='managers'),
    path('manager/<slug:slug>/', views.profile, name='profile'),
    path('team/<slug:slug>/', views.club, name='team'),
    path('seasons/list', views.SeasonListView.as_view(), name='season-list'),
    path('season/<slug:slug>/', views.season, name='season'),
    path('country/<int:country_id>/', views.country, name='country'),
    
    path('news/', views.news, name='news'),
    path('search/', views.search, name='search'),
    
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
