from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fam', 'name', 'otc', 'phone')


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'spring', 'summer', 'autumn')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('title', 'data')


class ImagesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('pk', 'pereval', 'title', 'data', 'added_date')


class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer(required=False)
    pk = serializers.IntegerField(required=False, read_only=True)
    images = ImagesViewSerializer(many=True, required=False)

    class Meta:
        model = Added
        fields = ('pk', 'beauty_title', 'title', 'other_titles',
                  'connect', 'add_time',
                  'user', 'coords', 'level', 'images')


class SubmitDataSerializer(PerevalSerializer):

    def create(self, validated_data):
        coord_data = validated_data.pop('coords')
        coords = Coords.objects.create(**coord_data)
        level_data = validated_data.pop('level')
        level = Level.objects.create(**level_data)
        user_data = validated_data.pop('user')
        user = User.objects.get_or_create(**user_data)
        tourist = User.objects.get(**user_data)
        images_data = None
        if 'images' in self.initial_data:
            images_data = validated_data.pop('images')
        pereval = Added.objects.create(coords=coords, level=level, user=tourist, **validated_data)
        if images_data:
            for data in images_data:
                Images.objects.create(pereval=pereval, **data)
        return pereval


