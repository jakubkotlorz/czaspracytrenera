from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import datetime, date, timedelta
from math import floor

from .models import Manager, Country, Season, Employment, City, Team, ExternalLink
from .forms import SearchForm, SeasonCreateForm, SeasonUpdateForm, SeasonAvanceForm, UploadFileForm
from .files_handling import upload_photo
from articles.models import Article


def index(request):
    context = {
        'articles': Article.published.all(),
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
        'all_managers': Manager.objects.all().order_by('name_last'),
        'recently_added': Manager.objects.all().order_by('-id')[0:10]
    } 
    if request.user.is_authenticated:
        context['admin_bar'] = True
    
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
    
    city = City.objects.get(pk=person.city_birth_id) if person.city_birth_id else ''

    history = person.jobs.order_by('-still_hired', '-date_finish')
    q_links = Q()
    for job in history:
        if job.still_hired is False and job.days_lasted:
            job.days = job.days_lasted
        else:
            job.days = (date.today() - date(year=job.date_start.year, month=job.date_start.month, day=job.date_start.day)).days
        if job.links:
            q_links = q_links | Q(job=job)
    links = ExternalLink.objects.filter(q_links) if len(q_links) > 0 else []
    current_job = history[0] if history and history[0].still_hired else ""
    season = current_job.getSeason() if current_job else None     
    
    context = { 'season': season, 'person': person, 'nationality': country, 'history': history, 'current_job': current_job, 'city': city, 'age': age, 'links': links, 'no_club_icon': Team().getIcon }
    context['admin_bar'] = True if request.user.is_authenticated else False
    context['managed_teams'] = ', '.join(set([job.team.name_full for job in history])) 
    context['league_managers'] = season.getThisSeasonManagers() if season else None
    return render(request, 'managers/profile.html', context)


@login_required
def profile_photo_view(request, slug):
    person = get_object_or_404(Manager, slug=slug)
    uploaded_file_url = None 
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file_url = upload_photo(request.FILES['file'])
            person.photo = uploaded_file_url
            person.save()
    else:
        form = UploadFileForm()
    context = { 'person': person, 'uploaded_file_url': uploaded_file_url, 'form': form }
    return render(request, 'managers/profile-update-photo.html', context)


class PersonalDataProfileView(LoginRequiredMixin, UpdateView):
    model = Manager
    fields = ('name_first', 'name_last', 'slug', 'country', 'date_birth', 'city_birth')
    template_name = 'managers/profile-update-personal.html'
    login_url = '/admin/'


class PersonAddView(LoginRequiredMixin, CreateView):
    model = Manager
    fields = ('name_first', 'name_last', 'country', 'date_birth', 'city_birth')
    template_name = 'managers/person-add.html'
    login_url = '/admin/'


class SeasonListView(ListView):
    template_name = 'managers/season_list.html'
    queryset = Season.currentSeasons.all()

    def get_context_data(self, **kwargs):
        context = super(SeasonListView, self).get_context_data(**kwargs)
        showHidden = self.request.GET.get('showHidden', False)
        if showHidden == 'True':
            context['hidden'] = Season.objects.filter(current=False)
        if self.request.user.is_authenticated:
            context['admin_bar'] = True
        return context


class SeasonCreateView(LoginRequiredMixin, CreateView):
    template_name = 'managers/season_create.html'
    login_url = '/admin/'
    form_class = SeasonCreateForm
    queryset = Season.objects.all()


class SeasonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'managers/season_update.html'
    login_url = '/admin/'
    form_class = SeasonUpdateForm
    queryset = Season.objects.all()

    def get_object(self):
        return get_object_or_404(Season, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(SeasonUpdateView, self).get_context_data(**kwargs)
        return context

    def clean(self):
        if 'add-team' in self.data:
            print('chcemy dodac druzyne')


def pkList2objectList(pkList, klass):
    """Helper function to cast list of returned ids (from POST) to a list of objects of klass."""
    retList = []
    for item in pkList:
        retList.append(klass.objects.get(pk=int(item)))
    return retList


@login_required
def season_avance(request, slug):
    previous = get_object_or_404(Season, slug=slug)
    
    previous_teams = previous.getTeamsInSeason()
    possible_teams = previous.getCountryTeamsNotInSeason()

    form = SeasonAvanceForm(
        request.POST or None,
        previous_teams = previous_teams,
        possible_teams = possible_teams,
        slug = slug,
    )

    if request.method == 'POST':
        if form.is_valid():
            relegated = pkList2objectList(request.POST.getlist('last_season_teams'), Team)
            promoted = pkList2objectList(request.POST.getlist('considered_teams'), Team)
            new_teams = (set(previous_teams) | set(promoted)) - set(relegated)

            new_season = Season.objects.create(
                country = previous.country,
                name = form.cleaned_data.get('name'),
                years = form.cleaned_data.get('years'),
                date_start = form.cleaned_data.get('date_start'),
                date_end = form.cleaned_data.get('date_end'),
                prev_season = previous,
            )
            new_season.teams.set(new_teams)
            
            # old season should point to new one
            previous.next_season = new_season
            previous.save()

            # display new season
            return redirect('managers:season', slug=new_season.slug)
        else:
            print("FORM IS NOT VALID!: ", form.errors)
    else:
        form.initial = {
                'prev_season': previous.prev_season,
                'name': previous.name,
                'date_start': previous.date_end + timedelta(days=1),
                'date_end': previous.date_end + timedelta(days=365),
            }

    context = {
        'previous': previous,
        'form': form
    }
    return render(request, 'managers/season_avance.html', context)


class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    model = Season
    success_url = reverse_lazy('managers:season-list')


def season_set_current(request, slug):
    season = get_object_or_404(Season, slug=slug)
    season.setNewCurrent()
    return redirect('managers:season', slug) 


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
    if request.user.is_authenticated:
        context['admin_bar'] = True
        context['avance_season'] = True if season.next_season is None else False
        context['next_season'] = season.next_season
        context['prev_season'] = season.prev_season
        context['next_season_slug'] = season.next_season.slug if season.next_season else False
        context['prev_season_slug'] = season.prev_season.slug if season.prev_season else False
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
