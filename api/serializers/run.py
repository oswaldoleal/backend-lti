from api.models import Run
from rest_framework import serializers
from datetime import datetime, timezone


class RunSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    minutes = serializers.SerializerMethodField("get_remaining_minutes")
    seconds = serializers.SerializerMethodField("get_remaining_seconds")

    def get_remaining_minutes(self, obj: Run):
        if obj.end_date <= datetime.now(timezone.utc):
            return 0
        return (obj.end_date - datetime.now(timezone.utc)).seconds // 60

    def get_remaining_seconds(self, obj: Run):
        if obj.end_date <= datetime.now(timezone.utc):
            return 0
        return (obj.end_date - datetime.now(timezone.utc)).seconds % 60

    class Meta:
        model = Run
        fields = [
            'start_date',
            'end_date',
            'id',
            'user_input',
            'minutes',
            'seconds',
        ]
