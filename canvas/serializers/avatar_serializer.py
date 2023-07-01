from rest_framework import serializers

from canvas.models.avatar_config import AvatarConfig


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarConfig
        fields = '__all__'
