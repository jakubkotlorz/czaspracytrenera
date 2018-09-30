from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from datetime import datetime, date, timedelta
from math import floor

from .models import Manager, Country, Season, Employment, TeamSeason, City, Team


def index(request):
    countries_list = Country.objects.order_by('id')
    cups_list = Season.objects.filter(current=True)
    context = { 'countries_list': countries_list, 'cups_list': cups_list }
    return render(request, 'managers/index.html', context)

def country(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    managers = Manager.objects.filter(country=country_id)
    seasons = Season.objects.filter(country=country_id)
    context = { 'country': country, 'managers': managers, 'cups': seasons }
    return render(request, 'managers/country.html', context) 

def profile(request, manager_id):
    person = get_object_or_404(Manager, pk=manager_id)
    age = floor((datetime.now().date() - person.date_birth).days/365.25)
    country = get_object_or_404(Country, pk=person.country_id)
    city = get_object_or_404(City, pk=person.city_birth_id)
    history = Employment.objects.filter(manager=manager_id)
    for job in history:
        job.days = (date.today() - date(year=job.date_start.year, month=job.date_start.month, day=job.date_start.day)).days    
    context = { 'person': person, 'nationality': country, 'history': history, 'city': city, 'age': age }
    return render(request, 'managers/profile.html', context)

def season(request, cup_id):
    season = get_object_or_404(Season, pk=cup_id)
    teamSeason = TeamSeason.objects.filter(season=cup_id)
    team_ids = [i.team_id for i in teamSeason]
    q_jobs = Q()
    q_team = Q()
    for team_id in team_ids:
        q_jobs = q_jobs | Q(team=team_id)
        q_team = q_team | Q(id=team_id)
    current_jobs = Employment.objects.filter(q_jobs).filter(still_hired=True)
    for job in current_jobs:
        job.days = (date.today() - date(year=job.date_start.year, month=job.date_start.month, day=job.date_start.day)).days
    teams = Team.objects.filter(q_team)
    context = { 'cup': season, 'teams': teams, 'current_jobs': current_jobs }
    return render(request, 'managers/season.html', context)

def club(request, club_id):
    pass