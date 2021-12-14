from rest_framework import serializers

from .models import EventStats


class ListEventStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStats
        fields = ('date_recorded', 'views', 'clicks', 'click_cost', 'cpc', 'cpm')


class EventStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStats
        fields = ('date_recorded', 'views', 'clicks', 'click_cost')
