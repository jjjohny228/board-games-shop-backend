import os
import sys
import django
from django.db import transaction


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings') # Укажи свой проект
django.setup()


from games.models import (
    Type, PlayerCount, AgeGroup, DifficultyLevel, Genre, Mechanic, Duration, Game, Publisher
)

# Додавання основних категорій
TYPES = ["Стратегічні", "Кооперативні", "Економічні", "Військові", "Детективні"]
PLAYER_COUNTS = ["Для 1 гравця", "Для 2 гравців", "Для 3-4 гравців", "Для 5+ гравців"]
AGE_GROUPS = ["Для дітей (3-6 років)", "Для дітей (7-12 років)", "Для підлітків і дорослих (12+)"]
DIFFICULTIES = ["Легкі", "Середньої складності", "Складні"]
GENRES = ["Фентезі", "Наукова фантастика", "Жахи", "Детективи", "Кіберпанк"]
MECHANICS = ["Кидання кубиків", "Колодобудівля", "Контроль територій", "Блеф", "Дедукція"]
DURATIONS = ["15-30 хвилин", "30-60 хвилин", "1-2 години"]


with transaction.atomic():
    for name in TYPES:
        Type.objects.get_or_create(name=name)
    for name in PLAYER_COUNTS:
        PlayerCount.objects.get_or_create(name=name)
    for name in AGE_GROUPS:
        AgeGroup.objects.get_or_create(name=name)
    for name in DIFFICULTIES:
        DifficultyLevel.objects.get_or_create(name=name)
    for name in GENRES:
        Genre.objects.get_or_create(name=name)
    for name in MECHANICS:
        Mechanic.objects.get_or_create(name=name)
    for name in DURATIONS:
        Duration.objects.get_or_create(name=name)

# Створення видавця
publisher, _ = Publisher.objects.get_or_create(name="GameMasters")

# Додавання ігор
GAMES = [
    {"title": "Magic Quest", "type": ["Стратегічні"], "genres": ["Фентезі", "Детективи"], "mechanics": ["Кидання кубиків"]},
    {"title": "Cyber Wars", "type": ["Військові"], "genres": ["Кіберпанк", "Наукова фантастика"], "mechanics": ["Колодобудівля"]},
    {"title": "Detective Club", "type": ["Детективні"], "genres": ["Детективи"], "mechanics": ["Дедукція", "Блеф"]},
    {"title": "Space Colony", "type": ["Економічні"], "genres": ["Наукова фантастика", "Детективи"], "mechanics": ["Контроль територій"]},
    {"title": "Dark Dungeon", "type": ["Детективні"], "genres": ["Детективи", "Фентезі"], "mechanics": ["Кидання кубиків"]},
    {"title": "Pirates' Gold", "type": ["Стратегічні"], "genres": ["Фентезі", "Детективи"], "mechanics": ["Колодобудівля", "Блеф"]},
    {"title": "Wild West Showdown", "type": ["Військові"], "genres": ["Жахи", "Детективи"], "mechanics": ["Контроль територій"]},
    {"title": "Medieval Kingdoms", "type": ["Стратегічні"], "genres": ["Детективи", "Детективи"], "mechanics": ["Контроль територій", "Ресурсний менеджмент"]},
    {"title": "Apocalypse Survival", "type": ["Кооперативні"], "genres": ["Жахи", "Детективи"], "mechanics": ["Кидання кубиків", "Дедукція"]},
    {"title": "Galactic Empires", "type": ["Стратегічні", "Кооперативні"], "genres": ["Жахи", "Детективи"], "mechanics": ["Контроль територій", "Колодобудівля"]},
]

with transaction.atomic():
    for game_data in GAMES:
        game = Game.objects.create(
            title=game_data["title"],
            description=f"Гра {game_data['title']} - захоплююча гра у жанрі {', '.join(game_data['genres'])}",
            rules_summary="Правила гри будуть додані пізніше.",
            release_year=2023,
            price=500,
            discount_price=450,
            stock=10,
            publisher=publisher,
            player_count=PlayerCount.objects.get(name="Для 3-4 гравців"),
            age_group=AgeGroup.objects.get(name="Для підлітків і дорослих (12+)"),
            difficulty=DifficultyLevel.objects.get(name="Середньої складності"),
            duration=Duration.objects.get(name="30-60 хвилин"),
        )
        print(Genre.objects.filter(name__in=game_data["genres"]))
        game.genre.set(Genre.objects.filter(name__in=game_data["genres"]))
        game.mechanic.set(Mechanic.objects.filter(name__in=game_data["mechanics"]))
        game.type.set(Type.objects.filter(name__in=game_data["type"]))
