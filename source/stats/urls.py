from django.urls import path
from . import views

urlpatterns = [
    path('get_event_stats', views.ListEventsStatsSortedView.as_view(), name="get_event_stats_sorted"),
    path('get_events', views.ListAllEventsStatsView.as_view(), name="get_event_stats"),
    path('create_event_stats', views.CreateEventStatsView.as_view(), name="create_event_stats"),
    path('delete_events', views.DeleteEventStatsView.as_view(), name="delete_event_stats"),
]
