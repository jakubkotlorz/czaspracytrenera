from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from datetime import datetime, date, timedelta
from math import floor

from .models import Manager, Country, Season, Employment, TeamSeason, City, Team, ExternalLink


def index(request):
    context = {
        'cups_list': Season.objects.filter(current=True),
    }
    return render(request, 'managers/index.html', context)

def news(request):
    context = {}
    return render(request, 'managers/news.html', context)

def managers(request):
    countries_list = Country.objects.order_by('-importance', 'name_en')
    for country in countries_list:
        country.count_managers = Manager.objects.filter(country=country).count()
    context = {
        'countries_list': countries_list,
        'all_managers': Manager.objects.all().order_by('name_last')
    }    
    return render(request, 'managers/managers-main.html', context)

def country(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    managers = Manager.objects.filter(country=country_id)
    seasons = Season.objects.filter(country=country_id)
    context = { 'country': country, 'managers': managers, 'cups': seasons }
    return render(request, 'managers/country.html', context) 

def profile(request, manager_id):
    person = get_object_or_404(Manager, pk=manager_id)
    if person.date_birth:
        if person.date_death:
            age = floor((person.date_death - person.date_birth).days/365.25)
        else:
            age = floor((datetime.now().date() - person.date_birth).days/365.25)
    else:
        age = ''
    country = get_object_or_404(Country, pk=person.country_id)
    if person.city_birth_id:
        city = City.objects.get(pk=person.city_birth_id)
    else:
        city = ''
    history = person.jobs.order_by('-still_hired', '-date_finish')
    q_links = Q()
    for job in history:
        if job.still_hired is False and job.days_lasted:
            job.days = job.days_lasted
        else:
            job.days = (date.today() - date(year=job.date_start.year, month=job.date_start.month, day=job.date_start.day)).days
        if job.links:
            q_links = q_links | Q(job=job)
    links = ExternalLink.objects.filter(q_links)
    if history and history[0].still_hired:
        current_job = history[0]
    else:
        current_job = ""
    context = { 'person': person, 'nationality': country, 'history': history, 'current_job': current_job, 'city': city, 'age': age, 'links': links, 'no_club_icon': Team().getIcon }
    return render(request, 'managers/profile.html', context)

def season(request, cup_id):
    season = get_object_or_404(Season, pk=cup_id)
    teamsInSeason = season.teams.all()
    team_ids = [i.team_id for i in teamsInSeason]
    q_team = Q()
    q_jobs = Q()
    for team_id in team_ids:
        q_team = q_team | Q(id=team_id)
        q_jobs = q_jobs | Q(team=team_id)
    teams = Team.objects.filter(q_team)

    jobs_season = Employment.objects.filter(q_jobs)
    jobs_lost = jobs_season.filter(date_finish__range=[season.date_start, season.date_end]).all()
    context = { 'cup': season, 'teams': teams, 'jobs_lost': jobs_lost }
    return render(request, 'managers/season.html', context)

def club(request, club_id):
    club = get_object_or_404(Team, pk=club_id)
    jobs = Employment.objects.filter(team=club.id).filter(role='1st').order_by('-still_hired', '-date_finish')
    for job in jobs:
        if job.still_hired:
            job.days = job.daysToday()
        else:
            job.days = job.days_lasted
    context = { 'club': club, 'history': jobs  }
    return render(request, 'managers/club.html', context)