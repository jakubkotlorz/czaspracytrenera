from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=3)
    name_pl = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10)


class City(models.Model):
    name_pl = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)


class Season(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10, default='default_cup200.png', blank=False)
    current = models.BooleanField(null=False, blank=False, default=False)


class Team(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name_full = models.CharField(max_length=50)
    name_short = models.CharField(max_length=20)


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)


class Manager(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    name_first = models.CharField(max_length=20)
    name_last = models.CharField(max_length=30)
    date_birth = models.DateTimeField(null=True, blank=True)
    city_birth = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)


class Employment(models.Model):
    FIRST = '1st'
    ASSISTANT = '2nd'
    ROLE_CHOICES = (
        (FIRST, 'First'),
        (ASSISTANT, 'Assistant'),
    )
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_start = models.DateTimeField(null=True, blank=True)
    date_finish = models.DateTimeField(null=True, blank=True)
    still_hired = models.BooleanField(null=False, blank=False, default=False)
    days_lasted = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=FIRST)
