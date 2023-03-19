from rest_framework import serializers

from pereval.models import Added, User, Coords, Level, Images


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Added
        fields = "__all__"


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


# class ImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Images
#         fields = ('title', 'data')


class SubmitDataSerializer(serializers.Serializer):
    user = UserSerializer()
    pass

