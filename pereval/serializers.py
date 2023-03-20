from rest_framework import serializers

from pereval.models import Added, User, Coords, Level, Images, Tourist


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Added
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    # fam = serializers.CharField()
    # name = serializers.CharField()
    # otc = serializers.CharField()
    # phone = serializers.CharField()

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


class SubmitDataSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer(required=False)
    pk = serializers.IntegerField(required=False)
    # images = ImagesSerializer(many=True)

    class Meta:
        model = Added
        fields = ('pk', 'beauty_title', 'title', 'other_titles',
                  'connect',# 'add_time',
                  'user', 'coords', 'level')#, 'images')

    def create(self, validated_data):
        coord_data = validated_data.pop('coords')
        coords = Coords.objects.create(**coord_data)
        level_data = validated_data.pop('level')
        level = Level.objects.create(**level_data)
        user_data = validated_data.pop('user')
        # images_data = validated_data.pop('images')
        pereval = Added.objects.create(coords=coords, level=level, **validated_data)
        # images = Images.objects.create(pereval=pereval, **images_data)
        user = User.objects.get_or_create(**user_data)
        tourist = User.objects.get(**user_data)
        tourist = Tourist.objects.create(tourist=tourist, pereval=pereval)
        return pereval

