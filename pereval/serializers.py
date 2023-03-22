from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
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
    data = serializers.ImageField(default=None)
    class Meta:
        model = Images
        fields = ('title', 'data')


class ImagesViewSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    data = serializers.ImageField(required=False)
    pereval = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Images
        fields = ('pk', 'pereval', 'title', 'data', 'added_date')


class SubmitDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesViewSerializer(many=True, required=False)

    class Meta:
        model = Added
        fields = ('__all__')
        depth = 1

    def create(self, validated_data):
        coord_data = validated_data.pop('coords')
        coords = Coords.objects.create(**coord_data)
        level_data = validated_data.pop('level')
        level = Level.objects.create(**level_data)
        user_data = validated_data.pop('user')
        user = Users.objects.get_or_create(**user_data)
        tourist = Users.objects.get(**user_data)
        images_data = None
        if 'images' in self.initial_data:
            images_data = validated_data.pop('images')
        pereval = Added.objects.create(coords=coords, level=level, user=tourist, **validated_data)
        if images_data:
            for data in images_data:
                Images.objects.create(pereval=pereval, **data)
        return pereval




