from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from datetime import datetime, date, timedelta
from math import floor

from .models import Manager, Country, Season, Employment, TeamSeason, City, Team, ExternalLink
from .forms import SearchForm


def index(request):
    context = {
        'cups_list': Season.objects.filter(current=True),
        'managers_hired': Employment.objects.filter(still_hired=True).order_by('-date_start')[:10],
        'managers_sacked': Employment.objects.filter(still_hired=False).order_by('-date_finish')[:10],
    }
    return render(request, 'managers/index.html', context)

def search_manager(search_text):
    res_query = Q()
    for q in search_text.split():
        if len(q) < 3:
            continue
        res_query = res_query | Q(name_first__contains=q) | Q(name_last__contains=q) | Q(slug__contains=q)

    if (len(res_query) > 0):
        return Manager.objects.filter(res_query)
    else:
        return []

def search_team(search_text):
    res_query = Q()
    for q in search_text.split():
        if len(q) < 2:
            continue
        res_query = res_query | Q(name_full__contains=q) | Q(name_short__contains=q)
    if (len(res_query) > 0):
        return Team.objects.filter(res_query)
    else:
        return []

def search(request):
    search_query = request.GET.get('q')

    if not search_query:  
        return redirect('managers:index') 

    context = {
        'query': search_query,
        'res_managers': search_manager(search_query),
        'res_teams': search_team(search_query),
    }

    return render(request, 'managers/search.html', context)

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

def profile(request, slug):
    person = get_object_or_404(Manager, slug=slug)
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
    other_teams = Team.objects.filter(country=season.country).exclude(q_team).order_by('-is_national')

    jobs_season = Employment.objects.filter(q_jobs)
    jobs_lost = jobs_season.filter(date_finish__range=[season.date_start, season.date_end]).all()
    context = { 'cup': season, 'teams': teams, 'jobs_lost': jobs_lost, 'other_teams': other_teams, 'country': season.country }
    return render(request, 'managers/season.html', context)

def club(request, club_id):
    club = get_object_or_404(Team, pk=club_id)
    jobs = Employment.objects.filter(team=club.id).filter(role='1st').order_by('-still_hired', '-date_finish')
    
    totalPeriodLength = int(365.25*20) # TODO: fix precision
    
    historyBegin = date.today() - timedelta(days=totalPeriodLength)

    clubTimeLine = []
    lastJobEndDate = historyBegin

    for job in reversed(jobs):
        # add new information for the table
        job.days = job.durationDays()

        # prepare club's timeline of managers

        # job older than we want to see
        if not job.still_hired and job.date_finish < historyBegin:
            continue

        # job started before and ended after history begin
        if job.date_start - historyBegin < timedelta(0):
            startOfJob = historyBegin
        else:
            startOfJob = job.date_start    
            # calculate previous duration of pause between managers
            lastPausePeriod = round((startOfJob - lastJobEndDate) / timedelta(days=totalPeriodLength) * 100)
            clubTimeLine.append({'isBreak': 'none', 'percentage': lastPausePeriod, 'text': ''})

        # save for next iteration - pause calculation
        lastJobEndDate = job.date_finish

        # calculate job duration
        daysPeriodStart = (startOfJob - historyBegin) / timedelta(days=totalPeriodLength)

        if job.still_hired:
            daysPeriodEnd = 1.0
        else:
            daysPeriodEnd = (lastJobEndDate - historyBegin) / timedelta(days=totalPeriodLength)
            if daysPeriodEnd < 0:
                daysPeriodEnd = 0
                continue
                
        jobPeriod = round((daysPeriodEnd - daysPeriodStart) * 100)

        # if period was short - show it as a pause! 1% of 20ys is 73d
        if jobPeriod < 2.0:
            clubTimeLine.append({'isBreak': 'none', 'percentage': jobPeriod, 'text': ''})
        else: 
            # prepare label depending on available bar size
            label = f"{job.manager.name_last[:round(jobPeriod*1.5)]}"
            clubTimeLine.append({'isBreak': '', 'percentage': jobPeriod, 'text': label})

    # print whole clubTimeLine
    s = 0
    for period in clubTimeLine:
        print('%30s %d | %s' % (period['text'], period['percentage'], period['isBreak']))
        s = s + period['percentage']
    print('suma tego wszystkiego: ', s)

    context = { 'club': club, 'history': jobs, 'clubTimeLine': clubTimeLine }
    return render(request, 'managers/club.html', context)
