from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.views.generic import CreateView, UpdateView

from datetime import datetime, date, timedelta
from math import floor

from .models import Manager, Country, Season, Employment, City, Team, ExternalLink
from .forms import SearchForm, SeasonCreateForm, SeasonUpdateForm


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
        res_query = res_query | Q(name_full__contains=q) | Q(name_short__contains=q) | Q(slug__contains=q)
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


class SeasonCreateView(CreateView):
    template_name = 'managers/season_create.html'
    form_class = SeasonCreateForm
    queryset = Season.objects.all()


class SeasonUpdateView(UpdateView):
    template_name = 'managers/season_update.html'
    form_class = SeasonUpdateForm
    queryset = Season.objects.all()

    def get_object(self):
        return get_object_or_404(Season, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(SeasonUpdateView, self).get_context_data(**kwargs)

        # season = get_object_or_404(Season, slug=self.kwargs['slug'])
        # thisCountryTeams = Team.objects.filter(country=season.country)
        # availableTeamsQs = thisCountryTeams.exclude(seasons=season)
        # # form = TeamToSeasonForm(availableTeamsQs, season.teams)

        # if self.request.method == 'POST':
        #     form = TeamToSeasonForm(availableTeamsQs, season.teams, self.request.POST)
        #     if form.is_valid():
        #         if form.cleaned_data['add_team']:
        #             season.teams.add(form.cleaned_data['add_team'])
        #         if form.cleaned_data['del_team']:
        #             season.teams.remove(form.cleaned_data['del_team'])
        # form = TeamToSeasonForm(availableTeamsQs, season.teams)        

        # context['update_team_list_form'] = form
        # context['cup'] = season
        print("KONTEKST: ", context)
        print("OBJEKT: ", type(context['object'].teams.all()))
        return context

    def clean(self):
        if 'add-team' in self.data:
            print('chcemy dodac druzyne')


def season(request, slug):
    season = get_object_or_404(Season, slug=slug)
    thisCountryTeams = Team.objects.filter(country=season.country)
    availableTeamsQs = thisCountryTeams.exclude(seasons=season)
    


    
    teamsInSeason = season.teams.all()
    otherTeams = list(set(thisCountryTeams) - set(teamsInSeason))
    
    # find jobs for given teams and filter to current season
    q_teams = Q()
    for t in teamsInSeason:
        q_teams.add(Q(team=t.pk), Q.OR)
    jobs_lost = Employment.objects.filter(q_teams).filter(date_finish__range=[season.date_start, season.date_end]) if len(q_teams) > 0 else []

    context = { 'cup': season, 'teams': teamsInSeason, 'jobs_lost': jobs_lost, 'other_teams': otherTeams, 'country': season.country }
    return render(request, 'managers/season.html', context)

def club(request, slug):
    club = get_object_or_404(Team, slug=slug)
    jobs = Employment.objects.filter(team=club.id).filter(role='1st').order_by('-still_hired', '-date_finish', '-date_start')
    
    totalPeriodLength = int(365.25*20) # TODO: fix precision
    
    historyBegin = date.today() - timedelta(days=totalPeriodLength)

    clubTimeLine = []
    lastJobEndDate = historyBegin

    for job in reversed(jobs):
        # add new information for the table
        job.days = job.durationDays()

        # job older than we want to see
        if not job.still_hired and job.date_finish < historyBegin:
            continue

        # calculate duration of pause preceeding current job
        if job.date_start - historyBegin < timedelta(0):
            startOfJob = historyBegin  # job started before and ended after history begin
        else:
            startOfJob = job.date_start
            pausePeriod = (startOfJob - lastJobEndDate) / timedelta(days=totalPeriodLength) * 100
            clubTimeLine.append({
                'percentage': floor(pausePeriod), 
                'rest': pausePeriod - floor(pausePeriod),
                'rest': 0,
                'text': '', 
                'isJob': 'no-job'
            })
        lastJobEndDate = job.date_finish # save for future pause calculation

        # calculate job duration
        daysPeriodStart = (startOfJob - historyBegin) / timedelta(days=totalPeriodLength)
        if job.still_hired:
            daysPeriodEnd = 1.0
        else:
            daysPeriodEnd = (lastJobEndDate - historyBegin) / timedelta(days=totalPeriodLength)
            if daysPeriodEnd < 0:
                daysPeriodEnd = 0
                print("Error! daysPeriodEnd < 0")
                continue       
        jobPeriod = (daysPeriodEnd - daysPeriodStart) * 100

        # prepare label depending on available bar size, 1% of 20ys is 73d
        label = f"{job.manager.name_last[:round(floor(jobPeriod)*1.5)]}"

        clubTimeLine.append({
            'percentage': floor(jobPeriod), 
            'rest': jobPeriod - floor(jobPeriod),
            'text': label,
            'isJob': 'job'
        })

    # prepare sorted list of rests (after floor)
    ids = [i for i,period in enumerate(clubTimeLine) if period['rest'] > 0]
    rests = sorted([({'id': r, 'rest': clubTimeLine[r]['rest']}) for r in ids], key=lambda k: k['rest'], reverse=True)

    # calculate and add padding
    if rests:
        padding = 100 - sum(item['percentage'] for item in clubTimeLine)
        for i in range(padding):
            k = rests[i % len(rests)]['id']
            clubTimeLine[k]['percentage'] = clubTimeLine[k]['percentage'] + 1

    # print whole clubTimeLine
    for period in clubTimeLine:
        del period['rest']
        # print(period)

    context = { 'club': club, 'history': jobs, 'clubTimeLine': clubTimeLine }
    return render(request, 'managers/club.html', context)
