from .models import EventStats


def get_sorted_event_stats(field_to_sort, last_date, start_date):
    return EventStats.objects.get_sorted_event_stats(field_to_sort, start_date, last_date)


def delete_all_event_stats():
    all_events = EventStats.objects.all()
    all_events.delete()


def get_all_event_stats():
    return EventStats.objects.all()
