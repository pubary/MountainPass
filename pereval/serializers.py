from rest_framework import serializers

from pereval.models import Added


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Added
        fields = "__all__"



