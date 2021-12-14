from django.db.models import Q

from .models import EventStats


def get_sorted_event_stats(field_to_sort, last_date, start_date):
    date_query_mask = Q(date_recorded__gte=start_date) & Q(date_recorded__lte=last_date)
    events_between_dates = EventStats.objects.filter(date_query_mask)
    return events_between_dates.order_by('date_recorded', field_to_sort)


def delete_all_event_stats():
    all_events = EventStats.objects.delete()
    all_events.delete()


def get_all_event_stats():
    return EventStats.objects.all()
