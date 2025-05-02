from datetime import datetime

from django.core.files import images
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .models import Game, Image, Genre, DifficultyLevel, Type, Mechanic, Duration, AgeGroup, PlayerCount, Publisher
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    # absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['path']

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        print(request)
        if request is not None:
            print("Request is not none")
            return request.build_absolute_uri(obj.path.url)
        return obj.path.url

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = '__all__'


class DifficultyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DifficultyLevel
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class PlayerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerCount
        fields = '__all__'


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)  # При GET-запросах отдаём полные объекты
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True  # При POST/PATCH принимаем список id
    )
    type = TypeSerializer(many=True, read_only=True)  # При GET-запросах отдаём полные объекты
    type_ids = serializers.PrimaryKeyRelatedField(
        queryset=Type.objects.all(), many=True, write_only=True  # При POST/PATCH принимаем список id
    )
    mechanic = MechanicSerializer(many=True, read_only=True)  # При GET-запросах отдаём полные объекты
    mechanic_ids = serializers.PrimaryKeyRelatedField(
        queryset=Mechanic.objects.all(), many=True, write_only=True  # При POST/PATCH принимаем список id
    )
    difficulty = DifficultyLevelSerializer(many=False, read_only=True)
    difficulty_id = serializers.PrimaryKeyRelatedField(queryset=DifficultyLevel.objects.all(), source='difficulty', write_only=True)
    player_count = PlayerCountSerializer(many=False, read_only=True)
    player_count_id = serializers.PrimaryKeyRelatedField(queryset=PlayerCount.objects.all(), source='player_count',
                                                       write_only=True)
    age_group = AgeGroupSerializer(many=False, read_only=True)
    age_group_id = serializers.PrimaryKeyRelatedField(queryset=AgeGroup.objects.all(), source='age_group',
                                                       write_only=True)
    duration = DurationSerializer(many=False, read_only=True)
    duration_id = serializers.PrimaryKeyRelatedField(queryset=Duration.objects.all(), source='duration',
                                                       write_only=True)
    publisher = PublisherSerializer(many=False, read_only=True)
    publisher_name = serializers.CharField(write_only=True)

    images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True,
        required=False
    )

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        genres = validated_data.pop('genre_ids', [])
        mechanics = validated_data.pop('mechanic_ids', [])
        types = validated_data.pop('type_ids', [])
        publisher_name = validated_data.pop('publisher_name', None)
        images_data = validated_data.pop('images', [])
        if publisher_name:
            publisher, _ = Publisher.objects.get_or_create(name=publisher_name)
            validated_data['publisher'] = publisher

        game = Game.objects.create(**validated_data)
        game.genre.set(genres)
        game.mechanic.set(mechanics)
        game.type.set(types)

        # Handle image uploads
        for image_file in images_data:
            Image.objects.create(game=game, path=image_file)
        return game

    def update(self, instance, validated_data):
        # Similar to create method, but for updating
        images_data = validated_data.pop('images', [])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle many-to-many fields if they're in the update
        if 'genre_ids' in validated_data:
            instance.genre.set(validated_data['genre_ids'])
        if 'mechanic_ids' in validated_data:
            instance.mechanic.set(validated_data['mechanic_ids'])
        if 'type_ids' in validated_data:
            instance.type.set(validated_data['type_ids'])

        # Handle image uploads
        if images_data:
            for image_file in images_data:
                try:
                    Image.objects.create(game=instance, path=image_file)
                except ValidationError as e:
                    print(f"Image validation error: {e}")

        return instance

    def validate_release_year(self, value):
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 2:
            raise serializers.ValidationError(_(f"Year must be between 1900 and {current_year + 2}"))
        return value

    def validate(self, data):
        if self.context['request'].method in ['POST', 'PUT']:
            if not data.get('genre_ids'):
                raise serializers.ValidationError({"genre_ids": _("This field cannot be empty.")})
            if not data.get('mechanic_ids'):
                raise serializers.ValidationError({"mechanic_ids": _("This field cannot be empty.")})
            if not data.get('type_ids'):
                raise serializers.ValidationError({"type_ids": _("This field cannot be empty.")})

        return data