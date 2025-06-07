import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from games.models import (
    Game, Image, Publisher, Type, PlayerCount,
    AgeGroup, DifficultyLevel, Genre, Mechanic, Duration
)


class Command(BaseCommand):
    help = 'Import 16 games from JSON data and add random images'
    def handle(self, *args, **options):
        images_dir = 'images_test'

        # Данные 16 игр
        games_data = [
            {
                "title": "Колонізатори",
                "description": "У грі 'Колонізатори' гравці змагаються за будівництво поселень, міст і доріг на змінному ігровому полі, торгуючи ресурсами, такими як дерево, цегла, вівці, пшениця та руда. Стратегічна торгівля та керування ресурсами є ключем до набору переможних очок.",
                "rules_summary": "Гравці кидають кубики для збору ресурсів, торгують із іншими та будують споруди. Перемагає той, хто першим набере 10 переможних очок.",
                "release_year": 1995,
                "price": Decimal("1499.00"),
                "discount_price": Decimal("1349.00"),
                "stock": 50,
                "publisher": "Kosmos",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Кидання кубиків"],
                "difficulty": "Середньої складності",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "1-2 години"
            },
            {
                "title": "Кодові імена",
                "description": "Командна словесна гра, де гравці дають підказки одним словом, щоб допомогти своїм товаришам по команді визначити своїх агентів на сітці слів.",
                "rules_summary": "Дві команди змагаються за визначення своїх таємних агентів на сітці 5x5. Шпигуни дають підказки одним словом, а товариші вгадують. Уникайте карти вбивці.",
                "release_year": 2015,
                "price": Decimal("599.00"),
                "discount_price": Decimal("539.00"),
                "stock": 60,
                "publisher": "Czech Games Edition",
                "types": ["Детективні"],
                "genres": ["Детективи"],
                "mechanics": ["Дедукція"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "15-30 хвилин"
            },
            {
                "title": "Темна гавань",
                "description": "Кооперативна тактична гра у фентезійному світі. Гравці беруть на себе ролі шукачів пригод, виконуючи квести та борючись із монстрами за допомогою унікальних здібностей.",
                "rules_summary": "Гравці обирають дії з карт персонажів, борються з ворогами та керують ресурсами. Сценарії пов'язані в кампанію, де рішення впливають на історію.",
                "release_year": 2017,
                "price": Decimal("4199.00"),
                "discount_price": Decimal("3899.00"),
                "stock": 10,
                "publisher": "Cephalofair Games",
                "types": ["Кооперативні"],
                "genres": ["Фентезі"],
                "mechanics": ["Дедукція"],
                "difficulty": "Складні",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "1-2 години"
            },
            {
                "title": "Суші Го!",
                "description": "Швидка карткова гра, де гравці збирають набори суші-карт, щоб набрати очки, балансуючи між стратегією та удачею.",
                "rules_summary": "Гравці вибирають карти з руки, передаючи решту наступному гравцеві. Очки нараховуються за зібрані набори суші. Гра складається з трьох раундів.",
                "release_year": 2013,
                "price": Decimal("449.00"),
                "discount_price": Decimal("399.00"),
                "stock": 80,
                "publisher": "Blue Orange Games",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Колодобудівля"],
                "difficulty": "Середньої складності",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Домініон",
                "description": "Гра на побудову колоди, де гравці створюють власну колоду карт, щоб отримувати переможні очки через покупку карт і керування ресурсами.",
                "rules_summary": "Гравці починають із маленької колоди та по черзі купують карти з центрального пулу, щоб покращити свою колоду. Гра закінчується, коли ключові стопки карт вичерпуються.",
                "release_year": 2008,
                "price": Decimal("1349.00"),
                "discount_price": Decimal("1199.00"),
                "stock": 25,
                "publisher": "Rio Grande Games",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Колодобудівля"],
                "difficulty": "Середньої складності",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Жах",
                "description": "Гравці працюють разом, щоб перемогти класичних кіномонстрів, таких як Дракула та Франкенштейн, рятуючи селян і виконуючи унікальні завдання.",
                "rules_summary": "Гравці переміщаються по дошці, збирають предмети та виконують завдання для перемоги над монстрами. Гра закінчується, коли всіх монстрів переможено.",
                "release_year": 2019,
                "price": Decimal("1199.00"),
                "discount_price": Decimal("1049.00"),
                "stock": 20,
                "publisher": "Ravensburger",
                "types": ["Кооперативні"],
                "genres": ["Жахи"],
                "mechanics": ["Дедукція"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Коса",
                "description": "Дія гри відбувається в альтернативній Європі 1920-х років, де гравці керують фракціями, змагаючись за контроль через керування ресурсами та бої.",
                "rules_summary": "Гравці розміщують працівників, збирають ресурси та будують механізми для контролю територій. Гра закінчується, коли гравець розміщує шосту зірку.",
                "release_year": 2016,
                "price": Decimal("2699.00"),
                "discount_price": Decimal("2399.00"),
                "stock": 15,
                "publisher": "Stonemaier Games",
                "types": ["Стратегічні"],
                "genres": ["Наукова фантастика"],
                "mechanics": ["Контроль територій"],
                "difficulty": "Складні",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "1-2 години"
            },
            {
                "title": "Одна ніч: Вовкулака",
                "description": "Швидка гра на обман, де гравцям призначаються таємні ролі селян або вовкулак. Гравці використовують здібності, щоб виявити вовкулак.",
                "rules_summary": "Гравці отримують карти ролей і виконують нічні дії таємно. Вдень вони голосують за підозрюваного вовкулака. Гра закінчується після одного циклу.",
                "release_year": 2014,
                "price": Decimal("749.00"),
                "discount_price": Decimal("674.00"),
                "stock": 30,
                "publisher": "Bezier Games",
                "types": ["Детективні"],
                "genres": ["Фентезі"],
                "mechanics": ["Колодобудівля"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Сутінки боротьби",
                "description": "Гра для двох гравців, що відтворює Холодну війну, де гравці керують США або СРСР, впливаючи на глобальні регіони через події.",
                "rules_summary": "Гравці розігрують карти подій і розподіляють очки операцій для поширення впливу. Гра закінчується після 10 ходів або при 20 очках.",
                "release_year": 2005,
                "price": Decimal("1799.00"),
                "discount_price": Decimal("1649.00"),
                "stock": 12,
                "publisher": "GMT Games",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Контроль територій"],
                "difficulty": "Складні",
                "player_count": "Для 5+ гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "1-2 години"
            },
            {
                "title": "Азул",
                "description": "Гравці вибирають кольорові плитки, щоб створювати мозаїчні візерунки на своїх дошках, отримуючи очки за стратегічне розміщення.",
                "rules_summary": "Гравці по черзі беруть плитки з центрального пулу та розміщують їх на своїй дошці. Очки нараховуються за завершені ряди.",
                "release_year": 2017,
                "price": Decimal("1199.00"),
                "discount_price": Decimal("1079.00"),
                "stock": 40,
                "publisher": "Plan B Games",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Контроль територій"],
                "difficulty": "Середньої складності",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Підземелля і дракони: Гнів Ашардлона",
                "description": "Кооперативна пригодницька гра, де гравці досліджують підземелля, борються з монстрами та виконують квести.",
                "rules_summary": "Гравці керують героями, рухаючись модульним підземеллям, борючись із монстрами. Кубики визначають результати бою.",
                "release_year": 2011,
                "price": Decimal("1949.00"),
                "discount_price": Decimal("1799.00"),
                "stock": 8,
                "publisher": "Kosmos",
                "types": ["Кооперативні"],
                "genres": ["Фентезі"],
                "mechanics": ["Кидання кубиків"],
                "difficulty": "Складні",
                "player_count": "Для 5+ гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "1-2 години"
            },
            {
                "title": "Карти проти всіх",
                "description": "Весела вечіркова гра, де гравці заповнюють пропуски в абсурдних твердженнях найсмішнішими відповідями.",
                "rules_summary": "Гравці по черзі читають чорну карту з підказкою. Інші подають білі карти, а читач обирає найсмішнішу.",
                "release_year": 2011,
                "price": Decimal("899.00"),
                "discount_price": Decimal("809.00"),
                "stock": 100,
                "publisher": "Bezier Games",
                "types": ["Детективні"],
                "genres": ["Фентезі"],
                "mechanics": ["Колодобудівля"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Зоряні війни: Повстання",
                "description": "Стратегічна гра про галактичний конфлікт, де гравці керують Альянсом повстанців або Галактичною імперією.",
                "rules_summary": "Гравці розгортають одиниці, виконують місії та керують ресурсами. Повстанці прагнуть повалити Імперію.",
                "release_year": 2016,
                "price": Decimal("2999.00"),
                "discount_price": Decimal("2699.00"),
                "stock": 10,
                "publisher": "Stonemaier Games",
                "types": ["Стратегічні"],
                "genres": ["Наукова фантастика"],
                "mechanics": ["Контроль територій"],
                "difficulty": "Складні",
                "player_count": "Для 3-4 гравців",
                "age_group": "Для підлітків і дорослих (12+)",
                "duration": "1-2 години"
            },
            {
                "title": "Тривіал Персьюіт",
                "description": "Класична вікторинна гра, де гравці відповідають на питання з різних категорій, щоб зібрати клини.",
                "rules_summary": "Гравці кидають кубик, щоб рухатися по дошці, відповідаючи на питання. Зберіть шість клинів, щоб виграти.",
                "release_year": 1981,
                "price": Decimal("1049.00"),
                "discount_price": Decimal("899.00"),
                "stock": 50,
                "publisher": "Ravensburger",
                "types": ["Детективні"],
                "genres": ["Детективи"],
                "mechanics": ["Дедукція"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "30-60 хвилин"
            },
            {
                "title": "Печворк",
                "description": "Гра для двох гравців, де учасники змагаються за створення найкращої клаптикової ковдри.",
                "rules_summary": "Гравці вибирають плитки та розміщують їх на своїй дошці, керуючи ґудзиками. Очки за завершені ковдри.",
                "release_year": 2014,
                "price": Decimal("899.00"),
                "discount_price": Decimal("809.00"),
                "stock": 35,
                "publisher": "Kosmos",
                "types": ["Стратегічні"],
                "genres": ["Фентезі"],
                "mechanics": ["Контроль територій"],
                "difficulty": "Легкі",
                "player_count": "Для 2 гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "15-30 хвилин"
            },
            {
                "title": "Розум",
                "description": "Кооперативна карткова гра, де гравці викладають карти в порядку зростання без спілкування.",
                "rules_summary": "Гравці викладають карти з рук у порядку зростання без розмов. Завершіть усі рівні, щоб перемогти.",
                "release_year": 2018,
                "price": Decimal("449.00"),
                "discount_price": Decimal("399.00"),
                "stock": 70,
                "publisher": "Ravensburger",
                "types": ["Кооперативні"],
                "genres": ["Фентезі"],
                "mechanics": ["Дедукція"],
                "difficulty": "Легкі",
                "player_count": "Для 5+ гравців",
                "age_group": "Для дітей (7-12 років)",
                "duration": "15-30 хвилин"
            }
        ]

        # Получаем список изображений
        full_images_path = os.path.join('games', images_dir)
        if not os.path.exists(full_images_path):
            self.stdout.write(
                self.style.ERROR(f'Папка с изображениями не найдена: {full_images_path}')
            )
            return

        image_files = []
        for file in os.listdir(full_images_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_files.append(os.path.join(full_images_path, file))

        if len(image_files) < 10:
            self.stdout.write(
                self.style.WARNING(
                    f'Найдено только {len(image_files)} изображений. Рекомендуется минимум 10.'
                )
            )

        # Создаем игры
        for game_data in games_data:
            try:
                # Создаем или получаем издателя
                publisher, _ = Publisher.objects.get_or_create(
                    name=game_data['publisher']
                )

                # Получаем связанные объекты
                difficulty = DifficultyLevel.objects.get(name=game_data['difficulty'])
                player_count = PlayerCount.objects.get(name=game_data['player_count'])
                age_group = AgeGroup.objects.get(name=game_data['age_group'])
                duration = Duration.objects.get(name=game_data['duration'])

                # Создаем игру
                game, created = Game.objects.get_or_create(
                    title=game_data['title'],
                    defaults={
                        'description': game_data['description'],
                        'rules_summary': game_data['rules_summary'],
                        'release_year': game_data['release_year'],
                        'price': game_data['price'],
                        'discount_price': game_data['discount_price'],
                        'stock': game_data['stock'],
                        'publisher': publisher,
                        'difficulty': difficulty,
                        'player_count': player_count,
                        'age_group': age_group,
                        'duration': duration,
                    }
                )

                if created:
                    self.stdout.write(f'Создана игра: {game.title}')

                    # Добавляем типы (many-to-many)
                    for type_name in game_data['types']:
                        game_type = Type.objects.get(name=type_name)
                        game.type.add(game_type)

                    # Добавляем жанры (many-to-many)
                    for genre_name in game_data['genres']:
                        genre = Genre.objects.get(name=genre_name)
                        game.genre.add(genre)

                    # Добавляем механики (many-to-many)
                    for mechanic_name in game_data['mechanics']:
                        mechanic = Mechanic.objects.get(name=mechanic_name)
                        game.mechanic.add(mechanic)

                    # Добавляем случайные изображения (до 10 штук)
                    if image_files:
                        num_images = min(10, len(image_files))
                        selected_images = random.sample(image_files, num_images)

                        for img_path in selected_images:
                            try:
                                with open(img_path, 'rb') as img_file:
                                    django_file = File(img_file)
                                    game_image = Image(game=game)
                                    game_image.path.save(
                                        os.path.basename(img_path),
                                        django_file,
                                        save=True
                                    )
                                self.stdout.write(
                                    f'  Добавлено изображение: {os.path.basename(img_path)}'
                                )
                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f'Ошибка при добавлении изображения {img_path}: {e}'
                                    )
                                )
                else:
                    self.stdout.write(f'Игра уже существует: {game.title}')

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Ошибка при создании игры {game_data["title"]}: {e}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f'Импорт завершен! Создано {len(games_data)} игр.')
        )
