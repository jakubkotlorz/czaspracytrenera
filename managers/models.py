from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.text import slugify


class Country(models.Model):
    code = models.CharField(max_length=3)
    name_pl = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    icon_name = models.CharField(max_length=10)
    importance = models.IntegerField(default=0)

    def get_flag(self):
        return f"{settings.MEDIA_URL}countries-flags/{self.icon_name}"

    def __str__(self):
        return self.name_pl


class City(models.Model):
    name_pl = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_pl    


class Team(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name_full = models.CharField(max_length=50, unique=True)
    name_short = models.CharField(max_length=20, unique=True)
    name_code = models.CharField(max_length=3, null=True, blank=True)
    icon_name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=55)
    is_national = models.BooleanField(default=False)

    def getIcon(self):
        if not self.icon_name:
            return f"/managers/icons-club/team.png"
        else:
            return f"/managers/icons-club/{self.country.code.lower()}/{self.icon_name}"

    def getCurrentEmployment(self):
        currentManager = self.hirings.filter(still_hired=True).filter(role='1st').first()
        return currentManager

    def getAllHirings(self):
        return self.hirings.order_by('-still_hired', '-date_finish')

    def __str__(self):
        return self.name_full

    def get_absolute_url(self):
        return reverse('managers:team', args=[str(self.slug)])


class CurrentSeasonsManager(models.Manager):
    def get_queryset(self):
        return super(CurrentSeasonsManager, self).get_queryset().filter(current=True)


class Season(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    years = models.CharField(max_length=20, null=True)
    slug = models.SlugField(max_length=55, unique=True, blank=True)
    icon_name = models.CharField(max_length=20, default='defaultcup_200.png', blank=False)
    current = models.BooleanField(null=False, blank=False, default=False)
    date_start = models.DateField(default=date(year=date.today().year, month=7, day=1))
    date_end = models.DateField(default=date(year=date.today().year + 1, month=6, day=30))
    jmb_bg1 = models.CharField(max_length=8, default="#505050")
    jmb_bg2 = models.CharField(max_length=8, default="#202020")
    jmb_col = models.CharField(max_length=8, default="#ffffff")
    teams = models.ManyToManyField(Team, related_name='seasons')
    next_season = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='prev')
    prev_season = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='next')

    objects = models.Manager()
    currentSeasons = CurrentSeasonsManager()

    def getTeamsInSeason(self):
        return self.teams.all()

    def getCountryTeamsNotInSeason(self, wo_national=False):
        teams = Team.objects.filter(country=self.country) \
            .exclude(seasons__pk=self.pk)
        if wo_national:
            teams = teams.filter(is_national=False)
        return teams

    def getThisSeasonManagers(self):
        return [team.getCurrentEmployment().manager for team in self.getTeamsInSeason() if team.getCurrentEmployment() is not None]

    def get_changes_amount(self):
        q_teams = models.Q()
        for t in self.getTeamsInSeason():
            q_teams.add(models.Q(team=t.pk), models.Q.OR)
        sacks = Employment.objects.filter(q_teams).filter(date_finish__range=[self.date_start, self.date_end])
        return len(sacks) if len(sacks) > 0 else '-'
    
    def get_cup_icon(self):
        return f"{settings.MEDIA_URL}cups-emblems/{self.icon_name}"

    def getCupList(self):
        """Returns a list of all prev and next seasons of this one."""
        cupList = []
        cup = self
        
        # rewind to latest season
        while(cup.next_season):
            cup = cup.next_season
        
        # build the list going to first one
        cupList.append(cup)
        while cup.prev_season:
            cup = cup.prev_season
            cupList.append(cup)

        return cupList

    def setNewCurrent(self):
        """Clear or currents in this cup and sets for this one."""
        for season in self.getCupList():
            if season.current:
                season.current = False
                season.save()
        self.current = True
        self.save()

    def __str__(self):
        return f"{self.name} {self.years}"

    def get_absolute_url(self):
        return reverse('managers:season', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify([self.name, self.years])
        super(Season, self).save(*args, **kwargs)


class Manager(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    name_first = models.CharField(max_length=20)
    name_last = models.CharField(max_length=30)
    date_birth = models.DateField(null=True, blank=True)
    city_birth = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    date_death = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=55)
    photo = models.CharField(max_length=50, null=True, blank=True)

    def getPhoto(self):
        img = self.photo if self.photo else "manager.png"
        return f"{settings.MEDIA_URL}photos/{img}"

    def __str__(self):
        return f"{self.name_first} {self.name_last}"

    def get_absolute_url(self):
        return reverse('managers:profile', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify([self.name_first, self.name_last])
        super(Manager, self).save(*args, **kwargs)



class Employment(models.Model):
    FIRST = '1st'
    ASSISTANT = '2nd'
    ROLE_CHOICES = (
        (FIRST, 'First'),
        (ASSISTANT, 'Assistant'),
    )

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='jobs')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='hirings')
    date_start = models.DateField(null=True, blank=True, default=date.today)
    date_finish = models.DateField(null=True, blank=True)
    still_hired = models.BooleanField(null=False, blank=False, default=False)
    days_lasted = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=FIRST)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['manager'], condition=models.Q(still_hired='True'), name='unique_manager_hired'),
            models.UniqueConstraint(fields=['team', 'role'], condition=models.Q(still_hired='True'), name='unique_team_hired')
    ]

    def getSeason(self):
        return self.team.seasons.first()

    def durationDays(self):
        if self.still_hired:
            return (date.today() - date(year=self.date_start.year, month=self.date_start.month, day=self.date_start.day)).days
        else:
            return self.days_lasted

    def save(self, *args, **kwargs):
        if self.date_start and self.date_finish and not self.still_hired:
            self.days_lasted = (
                date(year=self.date_finish.year, month=self.date_finish.month, day=self.date_finish.day)
                - date(year=self.date_start.year, month=self.date_start.month, day=self.date_start.day)
                ).days
        super(Employment, self).save(*args, **kwargs)

    def __str__(self):
        hired = "Hired" if self.still_hired else "NOT hired"
        return f"[{hired} {self.role}] [{self.team}] {self.manager} [{self.date_start}-{self.date_finish}]"


class ExternalLink(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=100, null=True, blank=True)
    job = models.ForeignKey(Employment, on_delete=models.CASCADE, null=True, blank=True, related_name='links')

    def __str__(self):
        return self.title
