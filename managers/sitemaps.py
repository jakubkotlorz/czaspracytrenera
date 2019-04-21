from django.contrib.sitemaps import Sitemap
from managers.models import Season, Team, Manager

class SeasonSitemap(Sitemap):

    def items(self):
        return Season.objects.all()


class TeamSitemap(Sitemap):

    def items(self):
        return Team.objects.all()


class ManagersSitemap(Sitemap):

    def items(self):
        return Manager.objects.all()
