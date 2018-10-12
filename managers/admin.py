from django.contrib import admin

from .models import Country, City, Manager, Season, Team, TeamSeason, Employment, ExternalLink


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


class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('manager', 'team', 'date_start', 'date_finish', 'still_hired', 'days_lasted', 'role')
    list_filter = ('still_hired', 'role')
    search_fields = ('manager', 'team')
    ordering = ['team__name_full', 'still_hired']
admin.site.register(Employment, EmploymentAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('country', 'name_full', 'name_short', 'name_code', 'icon_name')
    list_filter = ('country', )
    ordering = ['country', 'name_full']
admin.site.register(Team, ClubAdmin)


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'job')
admin.site.register(ExternalLink, ExternalLinkAdmin)
