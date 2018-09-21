from django.shortcuts import get_object_or_404, render

from .models import Manager, Country, Season, Employment


def index(request):
    countries_list = Country.objects.order_by('id')
    context = { 'countries_list': countries_list, }
    return render(request, 'managers/index.html', context)

def country(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    managers = Manager.objects.filter(country=country_id)
    seasons = Season.objects.filter(country=country_id)
    context = { 'country': country, 'managers': managers, 'cups': seasons}
    return render(request, 'managers/country.html', context) 

def profile(request, manager_id):
    person = get_object_or_404(Manager, pk=manager_id)
    country = get_object_or_404(Country, pk=person.country_id)
    history = Employment.objects.filter(manager=manager_id)
    context = { 'person': person, 'country': country, 'history': history }
    return render(request, 'managers/profile.html', context)