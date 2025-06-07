from django.core.management.base import BaseCommand
from games.models import Type, PlayerCount, AgeGroup, DifficultyLevel, Genre, Mechanic, Duration


class Command(BaseCommand):
    help = 'Populate reference tables for board games'

    def handle(self, *args, **options):
        # Types of games
        types_data = ["Стратегічні", "Кооперативні", "Економічні", "Військові", "Детективні"]
        for type_name in types_data:
            Type.objects.get_or_create(name=type_name)
        self.stdout.write(f'Создано {len(types_data)} типов игр')

        # Number of players
        player_counts_data = ["Для 1 гравця", "Для 2 гравців", "Для 3-4 гравців", "Для 5+ гравців"]
        for count in player_counts_data:
            PlayerCount.objects.get_or_create(name=count)
        self.stdout.write(f'Создано {len(player_counts_data)} вариантов количества игроков')

        # Age groups
        age_groups_data = ["Для дітей (3-6 років)", "Для дітей (7-12 років)", "Для підлітків і дорослих (12+)"]
        for age_group in age_groups_data:
            AgeGroup.objects.get_or_create(name=age_group)
        self.stdout.write(f'Создано {len(age_groups_data)} возрастных групп')

        # Levels of difficulty
        difficulties_data = ["Легкі", "Середньої складності", "Складні"]
        for difficulty in difficulties_data:
            DifficultyLevel.objects.get_or_create(name=difficulty)
        self.stdout.write(f'Создано {len(difficulties_data)} уровней сложности')

        # Genres
        genres_data = ["Фентезі", "Наукова фантастика", "Жахи", "Детективи", "Кіберпанк"]
        for genre in genres_data:
            Genre.objects.get_or_create(name=genre)
        self.stdout.write(f'Создано {len(genres_data)} жанров')

        # Mechanics
        mechanics_data = ["Кидання кубиків", "Колодобудівля", "Контроль територій", "Блеф", "Дедукція"]
        for mechanic in mechanics_data:
            Mechanic.objects.get_or_create(name=mechanic)
        self.stdout.write(f'Создано {len(mechanics_data)} механик')

        # Duration
        durations_data = ["15-30 хвилин", "30-60 хвилин", "1-2 години"]
        for duration in durations_data:
            Duration.objects.get_or_create(name=duration)
        self.stdout.write(f'Создано {len(durations_data)} вариантов продолжительности')

        self.stdout.write(
            self.style.SUCCESS('Все справочные таблицы успешно заполнены!')
        )
