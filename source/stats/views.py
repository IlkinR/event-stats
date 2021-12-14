from datetime import datetime

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status, exceptions
from rest_framework.response import Response

from .models import EventStats
from .serializers import ListEventStatsSerializer, EventStatsSerializer
from .services import get_sorted_event_stats, delete_all_event_stats, get_all_event_stats

AVAILABLE_EVENT_STATS_FIELDS = tuple(field.name for field in EventStats._meta.fields)


def to_date(date_string, dtformat='%Y-%m-%d'):
    return datetime.strptime(date_string, dtformat)


class ListEventsStatsView(ListAPIView):
    serializer_class = ListEventStatsSerializer
    model = EventStats

    def get_queryset(self):
        # Validating date queries
        start_date = self.request.query_params.get('from')
        last_date = self.request.query_params.get('to')
        if to_date(start_date) > to_date(start_date):
            fail_details = "Start date cann't be greater than end date!"
            raise exceptions.ParseError(fail_details)

        # Validating field wchich will be used for sorting
        field_to_sort = self.request.query_params.get('sortway')
        if field_to_sort not in AVAILABLE_EVENT_STATS_FIELDS:
            right_fields_msg = ', '.join(AVAILABLE_EVENT_STATS_FIELDS)
            fail_details = f"Cann't sort by {field_to_sort}. Right ones: {right_fields_msg}"
            raise exceptions.ParseError(fail_details)

        return get_sorted_event_stats(field_to_sort, last_date, start_date)


class CreateEventStatsView(CreateAPIView):
    queryset = get_all_event_stats()
    serializer_class = EventStatsSerializer


class DeleteEventStatsView(UpdateAPIView):
    queryset = get_all_event_stats()
    serializer_class = EventStatsSerializer

    def delete(self, request):
        delete_all_event_stats()
        return Response('Stats deleted!', status=status.HTTP_200_OK)
