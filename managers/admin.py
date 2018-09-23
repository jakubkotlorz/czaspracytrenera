from django.contrib import admin

from .models import Country, City, Manager, Season, Team, TeamSeason, Employment


class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_pl', 'name_en', 'icon_name')
admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name_pl', 'country')
admin.site.register(City, CityAdmin)