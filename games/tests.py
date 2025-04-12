import io
from ddf import G
from PIL import Image

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from games.models import Game, AgeGroup, Type, DifficultyLevel, Genre, Mechanic, Duration, Review, PlayerCount, Publisher

def create_image(height: int, width: int) -> SimpleUploadedFile:
    # Creates image with different sizes for tests
    valid_image = Image.new('RGB', (height, width), color='white')
    buffer = io.BytesIO()
    valid_image.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    return SimpleUploadedFile('cover.jpg', image_data, content_type='image/jpg')


class GameViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create admin user
        cls.admin_user = G(User, is_staff=True)

        # Create regular user
        cls.user = G(User)

        # Create related models
        cls.type_board = G(Type, name='board')
        cls.type_card = G(Type, name='card')
        cls.player_count_4 = G(PlayerCount, name='4 players')
        cls.player_count_6 = G(PlayerCount, name='6 players')
        cls.age_group_12 = G(AgeGroup, name='12+')
        cls.age_group_8 = G(AgeGroup, name='8+')
        cls.difficulty_medium = G(DifficultyLevel, name='medium')
        cls.difficulty_easy = G(DifficultyLevel, name='easy')
        cls.difficulty_hard = G(DifficultyLevel, name='hard')
        cls.genre_strategy = G(Genre, name='strategy')
        cls.genre_family = G(Genre, name='family')
        cls.genre_adventure = G(Genre, name='adventure')
        cls.mechanic_1 = G(Mechanic, name='deck building')
        cls.mechanic_2 = G(Mechanic, name='area control')
        cls.mechanic_3 = G(Mechanic, name='dice rolling')
        cls.mechanic_4 = G(Mechanic, name='worker placement')
        cls.duration_30 = G(Duration, name='30 minutes')
        cls.duration_60 = G(Duration, name='60 minutes')
        cls.duration_45 = G(Duration, name='45 minutes')
        cls.publisher = G(Publisher, name='Test Publisher')

        # Create sample games with different attributes
        cls.game1 = Game.objects.create(
            title='Strategy Game',
            description='A complex strategy game',
            price='50.00',
            discount_price='45.00',
            publisher=cls.publisher,
            player_count=cls.player_count_4,
            age_group=cls.age_group_12,
            difficulty=cls.difficulty_medium,
            duration=cls.duration_60,
            release_year=2022
        )
        cls.game1.type.add(cls.type_board)
        cls.game1.genre.add(cls.genre_strategy)
        cls.game1.mechanic.add(cls.mechanic_2)

        cls.game2 = Game.objects.create(
            title='Family Card Game',
            description='Fun for the whole family',
            price='20.00',
            discount_price='18.00',
            publisher=cls.publisher,
            player_count=cls.player_count_6,
            age_group=cls.age_group_8,
            difficulty=cls.difficulty_easy,
            duration=cls.duration_30,
            release_year=2022
        )
        cls.game2.type.add(cls.type_card)
        cls.game2.genre.add(cls.genre_family)
        cls.game2.mechanic.add(cls.mechanic_1)

        # Add a review to set a rating for game2
        Review.objects.create(
            game=cls.game2,
            user=cls.user,
            rating=4.8,
            comment="Great family game!"
        )

        # Define URL endpoints
        cls.list_url = reverse('games:game-list')
        cls.detail_url = reverse('games:game-detail', kwargs={'pk': cls.game1.pk})

        # Set up clients
        cls.admin_client = APIClient()
        cls.user_client = APIClient()

        # Create JWT tokens for both users
        cls.admin_refresh = RefreshToken.for_user(cls.admin_user)
        cls.admin_access = str(cls.admin_refresh.access_token)

        cls.user_refresh = RefreshToken.for_user(cls.user)
        cls.user_access = str(cls.user_refresh.access_token)

    def setUp(self):
        # This runs before each test method
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
        # Unauthenticated client will be self.client

    def test_list_games_unauthenticated(self):
        """Test that anyone can list games without authentication"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming we have 2 games

    def test_retrieve_game_unauthenticated(self):
        """Test that anyone can retrieve a game without authentication"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Strategy Game')

    def test_create_game_admin(self):
        """Test that admin can create a game"""
        data = {
            'title': 'New Game',
            'description': 'A newly created game',
            'price': '35.00',
            'publisher_name': "Some new publisher",
            'type_ids': [self.type_board.id],
            'player_count_id': self.player_count_4.id,
            'age_group_id': self.age_group_12.id,
            'difficulty_id': self.difficulty_hard.id,
            'genre_ids': [self.genre_adventure.id],
            'mechanic_ids': [self.mechanic_4.id],
            'duration_id': self.duration_45.id,
            'release_year': 2023,
            "images": [
                create_image(1000, 1500),
                create_image(800, 800)
            ]

        }
        response = self.admin_client.post(self.list_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_game_unauthorized(self):
        """Test that regular users cannot create a game"""
        data = {
            'title': 'New Game',
            'description': 'A newly created game',
            'price': '35.00',
            'publisher': self.publisher.id,
            'type': [self.type_board.id],
            'player_count': self.player_count_4.id,
            'age_group': self.age_group_12.id,
            'difficulty': self.difficulty_hard.id,
            'genre': [self.genre_adventure.id],
            'mechanic': [self.mechanic_4.id],
            'duration': self.duration_45.id,
            'release_year': 2023
        }
        # Test with regular user
        response = self.user_client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test with unauthenticated user
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_game_admin(self):
        """Test that admin can update a game"""
        data = {'title': 'Updated Game Title'}
        response = self.admin_client.patch(self.detail_url, data)
        response2 = self.admin_client.get(self.detail_url)
        print(response2.data)
        print('Response Status:', response.status_code)
        print('Response Data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Game Title')

    def test_update_game_unauthorized(self):
        """Test that regular users cannot update a game"""
        data = {'title': 'Hacked Game Title'}
        response = self.user_client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_game_admin(self):
        """Test that admin can delete a game"""
        response = self.admin_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Game.objects.filter(pk=self.game1.pk).exists())

    def test_delete_game_unauthorized(self):
        """Test that regular users cannot delete a game"""
        response = self.user_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_number_filters(self):
        """Test min_price and max_price filters"""
        # Test min_price
        response = self.client.get(f"{self.list_url}?min_price=30")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only game1 should match

        # Test max_price
        response = self.client.get(f"{self.list_url}?max_price=30")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only game2 should match

        # Test both together
        response = self.client.get(f"{self.list_url}?min_price=15&max_price=55")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both games should match

    def test_type_filter(self):
        """Test type filter"""
        response = self.client.get(f"{self.list_url}?type={self.type_board.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

    def test_player_count_filter(self):
        """Test player_count filter"""
        response = self.client.get(f"{self.list_url}?player_count={self.player_count_6.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')

    def test_age_group_filter(self):
        """Test age_group filter"""
        response = self.client.get(f"{self.list_url}?age_group={self.age_group_8.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')

    def test_difficulty_filter(self):
        """Test difficulty filter"""
        response = self.client.get(f"{self.list_url}?difficulty={self.difficulty_easy.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')

    def test_genre_filter(self):
        """Test genre filter"""
        response = self.client.get(f"{self.list_url}?genre={self.genre_strategy.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

    def test_mechanic_filter(self):
        """Test mechanic filter"""
        response = self.client.get(f"{self.list_url}?mechanic={self.mechanic_2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

    def test_duration_filter(self):
        """Test duration filter"""
        response = self.client.get(f"{self.list_url}?duration={self.duration_60.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

    def test_search(self):
        """Test search functionality"""
        # Search by title
        response = self.client.get(f"{self.list_url}?search=Strategy")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

        # Search by description
        response = self.client.get(f"{self.list_url}?search=family")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')

        # Search with no results
        response = self.client.get(f"{self.list_url}?search=nonexistent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_ordering(self):
        """Test ordering functionality"""
        # Test ordering by rating
        # Note: in a real app, you might need to calculate an average rating first
        response = self.client.get(f"{self.list_url}?ordering=rating")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test ordering by discount_price
        response = self.client.get(f"{self.list_url}?ordering=discount_price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')  # 18.00
        self.assertEqual(response.data[1]['title'], 'Strategy Game')  # 45.00

    def test_combined_filters(self):
        """Test combinations of filters, search, and ordering"""
        # Filter by price range + search + ordering
        url = f"{self.list_url}?min_price=10&max_price=100&search=game&ordering=discount_price"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Family Card Game')  # Lower price
        self.assertEqual(response.data[1]['title'], 'Strategy Game')  # Higher price

        # More specific combination
        url = f"{self.list_url}?min_price=30&type={self.type_board.id}&ordering=price"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Strategy Game')

    def test_filter_edge_cases(self):
        """Test edge cases for filters"""
        # Invalid filters should be ignored
        response = self.client.get(f"{self.list_url}?nonexistent_filter=value")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # All games returned

        # Empty value for number filter
        response = self.client.get(f"{self.list_url}?min_price=")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # All games returned

    def test_pagination(self):
        """Test pagination if implemented"""
        # Create more games to trigger pagination
        for i in range(10):
            game = Game.objects.create(
                title=f'Extra Game {i}',
                price='30.00',
                publisher=self.publisher,
                player_count=self.player_count_4,
                age_group=self.age_group_12,
                difficulty=self.difficulty_medium,
                duration=self.duration_45,
                release_year=2023
            )
            game.type.add(self.type_board)
            game.genre.add(self.genre_strategy)
            game.mechanic.add(self.mechanic_1)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if pagination is in the response
        if 'results' in response.data:
            # Pagination is enabled
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
            self.assertEqual(response.data['count'], 12)  # 2 original + 10 new games

            # Test going to next page
            next_url = response.data['next']
            if next_url:
                # Extract the path and query from the full URL
                path = next_url.split('http://testserver')[1]
                response = self.client.get(path)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
