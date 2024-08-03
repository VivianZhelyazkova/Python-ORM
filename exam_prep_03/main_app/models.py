from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.

from django.db import models

from main_app.managers import TennisPlayerManager


class TennisPlayer(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(5)])
    birth_date = models.DateField()
    country = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    ranking = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(300)])
    is_active = models.BooleanField(default=True)
    objects = TennisPlayerManager()

    def __str__(self):
        return f"Tennis Player: {self.full_name}, country: {self.country}, ranking: {self.ranking}"


class Tournament(models.Model):
    name = models.CharField(max_length=150, unique=True, validators=[MinLengthValidator(2)])
    location = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    prize_money = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    SURFACE_CHOICES = [
        ('Not Selected', 'Not Selected'),
        ('Clay', 'Clay'),
        ('Grass', 'Grass'),
        ('Hard Court', 'Hard Court'),
    ]
    surface_type = models.CharField(max_length=12, choices=SURFACE_CHOICES, default='Not Selected')


class Match(models.Model):
    score = models.CharField(max_length=100)
    summary = models.TextField(validators=[MinLengthValidator(5)])
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(TennisPlayer,related_name="matches")
    winner = models.ForeignKey(TennisPlayer, null=True, on_delete=models.SET_NULL, related_name='matches_won')

    class Meta:
        verbose_name_plural = "Matches"
