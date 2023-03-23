from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


class ImagesViewSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    data = serializers.ImageField(required=False)
    pereval = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Images
        fields = ('pk', 'pereval', 'title', 'data', 'added_date')


class SubmitDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer(required=False)
    level = LevelSerializer()
    images = ImagesViewSerializer(many=True, required=False)

    class Meta:
        model = Added
        fields = ('__all__')

    def create(self, validated_data):
        coord_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        user_data = validated_data.pop('user')
        images_data = None
        if 'images' in self.initial_data:
            images_data = validated_data.pop('images')
        coords = Coords.objects.create(**coord_data)
        level = Level.objects.create(**level_data)
        user = Users.objects.get_or_create(**user_data)
        tourist = get_object_or_404(queryset=Users.objects.all(), email=user_data['email'])
        pereval = Added.objects.create(coords=coords, level=level, user=tourist, **validated_data)
        if images_data:
            for image_data in images_data:
                Images.objects.create(pereval=pereval, **image_data)
        return pereval

    def update(self, instance, validated_data):
        if 'coords' in self.initial_data:
            coord_data = validated_data.pop('coords')
            if instance.coords:
                coords = instance.coords
                for (key, value) in coord_data.items():
                    setattr(coords, key, value)
                    coords.save()
            else:
                Coords.objects.create(**coord_data)
        if 'level' in self.initial_data:
            level_data = validated_data.pop('level')
            if instance.level:
                level = instance.level
                for (key, value) in level_data.items():
                    setattr(level, key, value)
                    level.save()
            else:
                Level.objects.create(**level_data)
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.save()
        return instance



