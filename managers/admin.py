from django.contrib import admin

from .models import Country, City, Manager, Season, Team, TeamSeason, Employment


class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_pl', 'name_en', 'icon_name')
admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name_pl', 'country')
admin.site.register(City, CityAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name_first', 'name_last', 'country', 'date_birth', 'city_birth', 'slug', 'photo')
    list_filter = ('country', )
    search_fields = ('name_first', 'name_last')
    prepopulated_fields = { 'slug': ('name_first', 'name_last', )}
    ordering = ['name_last', 'country']
admin.site.register(Manager, ManagerAdmin)
