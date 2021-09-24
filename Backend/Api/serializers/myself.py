from rest_framework import serializers

from Database.models import FinishAnimateModel


class FinishAnimateSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FinishAnimateModel
        fields = '__all__'
