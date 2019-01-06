from django.contrib import admin

from .models import Country, City, Manager, Season, Team, TeamSeason, Employment, ExternalLink


class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_pl', 'name_en', 'icon_name')
    list_display_links = ('name_pl', 'name_en')
admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name_pl', 'country')
admin.site.register(City, CityAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name_first', 'name_last', 'country', 'date_birth', 'city_birth', 'slug', 'photo')
    list_display_links = ('name_last', 'name_first')
    list_filter = ('country', )
    search_fields = ('name_first', 'name_last')
    prepopulated_fields = { 'slug': ('name_first', 'name_last', )}
    ordering = ['name_last', 'country']
admin.site.register(Manager, ManagerAdmin)


class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('manager', 'team', 'date_start', 'date_finish', 'still_hired', 'days_lasted', 'role')
    list_display_links = ('manager', 'team', 'date_start', 'date_finish', 'still_hired')
    list_filter = ('still_hired', 'role')
    search_fields = ('manager__name_first', 'manager__name_last', 'team__name_full', 'team__name_short')
    ordering = ['team__name_full', 'still_hired']
admin.site.register(Employment, EmploymentAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('is_national', 'country', 'name_full', 'name_short', 'name_code', 'icon_name')
    list_display_links = ('name_full', 'name_short', 'name_code')
    list_filter = ('country', 'is_national')
    ordering = ['country', 'name_full']
admin.site.register(Team, ClubAdmin)


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('current', 'name', 'years', 'country')
    list_display_links = ('name', 'years')
    list_filter = ('current', )
    ordering = ('country', )
admin.site.register(Season, SeasonAdmin)


class TeamSeasonAdmin(admin.ModelAdmin):
    list_display = ('season', 'team')
    list_display_links = ('team', )
admin.site.register(TeamSeason, TeamSeasonAdmin)


class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'job')
    list_display_links = ('title', )
admin.site.register(ExternalLink, ExternalLinkAdmin)
