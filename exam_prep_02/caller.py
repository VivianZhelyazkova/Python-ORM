import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Director, Actor
from django.db.models import Q, Count, Avg


# Import your models here

# Create queries within functions
def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""
    elif search_name is not None and search_nationality is None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')
    elif search_name is None and search_nationality is not None:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')
    else:
        directors = Director.objects.filter(
            Q(nationality__icontains=search_nationality) & Q(full_name__icontains=search_name)).order_by('full_name')
    if not directors.exists():
        return ""
    return "\n".join(str(d) for d in directors)


def get_top_director():
    top_director = Director.objects.annotate(movies_count=Count("director")).order_by("-movies_count",
                                                                                      "full_name").first()
    if not top_director.exists():
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."


def get_top_actor():
    actor = (Actor.objects.prefetch_related("starring_actor").annotate(
        movies_count=Count("starring_actor"), avg_rating=Avg("starring_actor__rating"))
             .order_by("-movies_count", "full_name").first())
    if not actor.exists() or not actor.movies_count:
        return ""
    movies = ", ".join(m.title for m in actor.starring_actor.all() if m)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.avg_rating:.1f}"
