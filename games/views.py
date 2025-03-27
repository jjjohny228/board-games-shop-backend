from django_filters import NumberFilter, BaseInFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import GameSerializer, ImageSerializer
from rest_framework import permissions
from .models import Game, Image
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
        if self.action in ['list', 'retrieve', 'images']:
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
        # print(images)
        print(Image.objects.all())
        serializer = ImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)
