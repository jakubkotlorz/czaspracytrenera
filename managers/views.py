from django.shortcuts import get_object_or_404, render

from .models import Manager, Country, Season, Employment, TeamSeason


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
    country = get_object_or_404(Country, pk=person.country_id)
    history = Employment.objects.filter(manager=manager_id)
    context = { 'person': person, 'country': country, 'history': history }
    return render(request, 'managers/profile.html', context)

def season(request, cup_id):
    season = get_object_or_404(Season, pk=cup_id)
    teams = TeamSeason.objects.filter(season=cup_id)
    context = { 'cup': season, 'teams': teams }
    return render(request, 'managers/season.html', context)