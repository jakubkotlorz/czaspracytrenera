from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=3)
    name_pl = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10)


class Season(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)


class Team(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name_full = models.CharField(max_length=50)
    name_short = models.CharField(max_length=20)


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)


class Manager(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name_first = models.CharField(max_length=20)
    name_last = models.CharField(max_length=30)


class Employment(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    