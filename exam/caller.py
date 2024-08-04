import os
import django
from django.db.models import Q, Count, Case, When, Value, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Astronaut, Mission, Spacecraft


# Import your models here

# Create queries within functions

def get_astronauts(search_string=None):
    if search_string is None:
        return ""
    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)).order_by('name')

    if not astronauts:
        return ""

    return "\n".join(str(a) for a in astronauts)


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()
    if not astronaut or not astronaut.missions_count:
        return "No data."
    return f"Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions."


def get_top_commander():
    commander = Astronaut.objects.annotate(num_commanded=Count("commanded_missions")).order_by(
        "-num_commanded", "phone_number").first()
    if not commander or not commander.num_commanded:
        return "No data."
    return f"Top Commander: {commander.name} with {commander.num_commanded} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.filter(status="Completed").order_by("-launch_date").first()
    if not mission:
        return "No data."
    astronauts = ", ".join(a.name for a in mission.astronauts.order_by("name"))
    spacewalks = sum(a.spacewalks for a in mission.astronauts.all())
    if mission.commander:
        commander = mission.commander.name
    else:
        commander = "TBA"
    return (f"The last completed mission is: {mission.name}. Commander: {commander}. Astronauts: {astronauts}."
            f" Spacecraft: {mission.spacecraft.name}. Total spacewalks: {spacewalks}.")


def get_most_used_spacecraft():
    most_used = Spacecraft.objects.annotate(
        num_missions=Count('mission')
    ).order_by('-num_missions', 'name').first()
    if most_used and most_used.num_missions > 0:
        num_astronauts = Astronaut.objects.filter(
            missions__spacecraft=most_used
        ).distinct().count()
        return f"The most used spacecraft is: {most_used.name}, manufactured by {most_used.manufacturer}, used in {most_used.num_missions} missions, astronauts on missions: {num_astronauts}."
    return "No data."


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(mission__status="Planned", weight__gte=200.0).distinct()

    affected_rows = spacecrafts.update(weight=F("weight") - 200.0)

    if affected_rows > 0:
        avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg("weight"))["avg_weight"]
        return f"The weight of {affected_rows} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    return "No changes in weight."
