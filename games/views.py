from django_filters import NumberFilter, BaseInFilter
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import GameSerializer, ImageSerializer, TypeSerializer, PlayerCountSerializer, AgeGroupSerializer, \
    DifficultyLevelSerializer, GenreSerializer, MechanicSerializer, DurationSerializer
from rest_framework import permissions
from .models import Game, Image, Duration, Mechanic, Genre, DifficultyLevel, AgeGroup, PlayerCount, Type
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class GameFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    genre = NumberInFilter(field_name="genre", lookup_expr="in")
    type = NumberInFilter(field_name="type", lookup_expr="in")
    mechanic = NumberInFilter(field_name="mechanic", lookup_expr="in")

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        str_min_price = self.data.get('min_price')
        str_max_price = self.data.get('max_price')
        min_price = float(str_min_price) if str_min_price else None
        max_price = float(str_max_price) if str_max_price else None
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValidationError("min_price can not be less than max_price.")
        if min_price is not None and min_price < 0:
            raise ValidationError("min_price cannot be less than 0.")
        if max_price is not None and max_price < 0:
            raise ValidationError("max_price cannot be less than 0.")

    class Meta:
        model = Game
        fields = [
            'type',
            'player_count',
            'age_group',
            'difficulty',
            'genre',
            'mechanic',
            'duration',
        ]


class GameModelViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = GameFilter
    ordering = ('-created_at',)
    ordering_fields = ['discount_price, created_at, rating']
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'images', 'all_categories']:
            permission_classes =  [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def images(self, request, pk=None):
        """
        Custom action to retrieve all images for a specific game
        """
        game = self.get_object()
        images = game.images.all()
        print(Image.objects.all())
        serializer = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def all_categories(self, request):
        """
        Return all categories and all sub categories

        """
        categories = [
            {
                'name': 'type',
                'display_name': _('Game type'),
                'values': TypeSerializer(Type.objects.all(), many=True).data
            },
            {
                'name': 'player_count',
                'display_name': _('Player count'),
                'values': PlayerCountSerializer(PlayerCount.objects.all(), many=True).data
            },
            {
                'name': 'age_group',
                'display_name': _('Age group'),
                'values': AgeGroupSerializer(AgeGroup.objects.all(), many=True).data
            },
            {
                'name': 'difficulty',
                'display_name': _('Difficulty level'),
                'values': DifficultyLevelSerializer(DifficultyLevel.objects.all(), many=True).data
            },
            {
                'name': 'genre',
                'display_name': _('Genres'),
                'values': GenreSerializer(Genre.objects.all(), many=True).data
            },
            {
                'name': 'mechanic',
                'display_name': _('Mechanics'),
                'values': MechanicSerializer(Mechanic.objects.all(), many=True).data
            },
            {
                'name': 'duration',
                'display_name': _('Duration'),
                'values': DurationSerializer(Duration.objects.all(), many=True).data
            }
        ]

        # Опционально: добавляем URL для фильтрации к каждому значению
        base_url = request.build_absolute_uri('/api/games/?')
        for category in categories:
            for value in category['values']:
                value['filter_url'] = f"{base_url}{category['name']}={value['id']}"

        return Response(categories)
