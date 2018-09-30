from django.db import models
from datetime import date

class Country(models.Model):
    code = models.CharField(max_length=3)
    name_pl = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name_pl


class City(models.Model):
    name_pl = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_pl    


class Season(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10, default='default_cup200.png', blank=False)
    current = models.BooleanField(null=False, blank=False, default=False)
    date_start = models.DateField(default=date(year=2018, month=7, day=1))
    date_end = models.DateField(default=date(year=2019, month=6, day=30))

class Team(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name_full = models.CharField(max_length=50)
    name_short = models.CharField(max_length=20)
    name_code = models.CharField(max_length=3, null=True, blank=True)
    icon_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name_full


class TeamSeason(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)


class Manager(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    name_first = models.CharField(max_length=20)
    name_last = models.CharField(max_length=30)
    date_birth = models.DateField(null=True, blank=True)
    city_birth = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=55)
    photo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name_first} {self.name_last}"


class Employment(models.Model):
    FIRST = '1st'
    ASSISTANT = '2nd'
    ROLE_CHOICES = (
        (FIRST, 'First'),
        (ASSISTANT, 'Assistant'),
    )
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_start = models.DateField(null=True, blank=True, default=date.today)
    date_finish = models.DateField(null=True, blank=True)
    still_hired = models.BooleanField(null=False, blank=False, default=False)
    days_lasted = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=FIRST)

    def save(self, *args, **kwargs):
        if self.date_start and self.date_finish and not self.still_hired:
            self.days_lasted = (
                date(year=self.date_finish.year, month=self.date_finish.month, day=self.date_finish.day)
                - date(year=self.date_start.year, month=self.date_start.month, day=self.date_start.day)
                ).days
        super(Employment, self).save(*args, **kwargs)

    def __str__(self):
        return f"[{self.still_hired} {self.role}] [{self.team}] {self.manager} [{self.date_start}-{self.date_finish}]"
