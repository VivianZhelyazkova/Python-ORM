from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager


# Create your models here.
class Base(models.Model):
    class Meta:
        abstract = True

    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default="Unknown")


class Director(Base):
    years_of_experience = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0)
    objects = DirectorManager()

    def __str__(self):
        return f"Director: {self.full_name}, nationality: {self.nationality}, experience:{self.years_of_experience}"


class Actor(Base):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    class GenreChoices(models.TextChoices):
        ACTION = "Action", "Action"
        COMEDY = "Comedy", "Comedy"
        DRAMA = "Drama", "Drama"
        OTHER = "Other", "Other"

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=6, default=GenreChoices.OTHER, choices=GenreChoices.choices)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0.0)
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name="director")
    starring_actor = models.ForeignKey(to=Actor, null=True, on_delete=models.SET_NULL, related_name="starring_actor")
    actors = models.ManyToManyField(Actor)
