import os
import django
from django.db.models import Count

from main_app.models import TennisPlayer, Tournament

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here

# Create queries within functions

def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    elif search_name is not None and search_country is None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)
    elif search_name is None and search_country is not None:
        players = TennisPlayer.objects.filter(country__icontains=search_country)
    else:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name, country__icontains=search_country)

    if not players:
        return ""

    players = players.order_by("ranking")
    return "\n".join(str(p) for p in players)


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if top_player is None:
        return ""
    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(matches_count=Count('matches')).order_by('-matches_count', 'ranking').first()
    if player is None or not player.matches_count:
        return ""

    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""
    tournaments = Tournament.objects.filter(surface_type__iconains == surface)
