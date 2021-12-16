import datetime
import random
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import EventStats


class TestEventStatsModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        EventStats.objects.create(date_recorded='2020-12-13', views=100, clicks=100, click_cost=100)
        EventStats.objects.create(date_recorded='2020-12-14', click_cost=100)

    def test_fields_have_properly_set(self):
        event_stats = EventStats.objects.get(pk=1)
        self.assertEqual(f'{event_stats.date_recorded}', "2020-12-13")
        self.assertEqual(event_stats.views, 100)
        self.assertEqual(event_stats.clicks, 100)
        self.assertEqual(event_stats.click_cost, 100)

    def test_even_stats_properties(self):
        event_stats = EventStats.objects.get(pk=1)
        self.assertEqual(event_stats.cpc, Decimal('1.00'))
        self.assertEqual(event_stats.cpm, Decimal('1000.00'))

    def test_even_stats_properties_invalid(self):
        event_stats = EventStats.objects.get(pk=2)
        self.assertIsNone(event_stats.cpc)
        self.assertIsNone(event_stats.cpm)

    def test_get_valid_ordered_queryset(self):
        test_data = [
            ('views', '2020-12-13', '2020-12-14'),
            ('clicks', '2020-12-13', '2020-12-14'),
            ('click_cost', '2020-12-13', '2020-12-14'),
        ]

        for field_to_sort, start_date, last_date in test_data:
            events = EventStats.objects.get_sorted_event_stats(field_to_sort, start_date, last_date)
            self.assertEqual(events.count(), 2)


class TestEventStatsView(TestCase):
    TOTAL_EVENTS_STATS_MODELS_COUNT = 4

    @classmethod
    def _next_date(cls, current_date_str):
        current_date = datetime.datetime.strptime(current_date_str, '%Y-%m-%d')
        date_tommrrow = current_date + datetime.timedelta(days=1)
        return date_tommrrow.strftime("%Y-%m-%d")

    @classmethod
    def setUpTestData(cls):
        start_date = '2021-12-13'
        created_models = 0

        while created_models < cls.TOTAL_EVENTS_STATS_MODELS_COUNT:
            EventStats.objects.create(
                date_recorded=start_date,
                views=random.randint(2, 100),
                clicks=random.randint(2, 100),
                click_cost=random.randint(2, 100),
            )
            start_date = cls._next_date(start_date)
            created_models += 1

    def test_get_ordered_event_stats(self):
        payload = {'from': '2021-12-13', 'to': '2021-12-15', 'sortway': 'views'}
        response = self.client.get(reverse('get_event_stats_sorted'), payload)
        self.assertEqual(response.status_code, 200)

    def _check_invalid_request(self, payload, urlname):
        response = self.client.get(reverse(urlname), payload)
        self.assertEqual(response.status_code, 400)

    def test_get_ordered_event_stats_invalid_queries(self):
        invalid_payloads = [
            {'from': '2021-12-13', 'sortway': 'views'},
            {'to': '2021-12-13', 'sortway': 'views'},
            {'from': '2021-12-13', 'to': '2021-12-15', 'sortway': 'likes'}
        ]

        for payload in invalid_payloads:
            self._check_invalid_request(payload, 'get_event_stats_sorted')

    def test_create_event_stats(self):
        payload = {
            "date_recorded": "2021-12-13",
            "views": 31273,
            "clicks": 312313123,
            "click_cost": 13
        }
        response = self.client.post(reverse('create_event_stats'), payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventStats.objects.count(), self.TOTAL_EVENTS_STATS_MODELS_COUNT + 1)

    def test_event_stats_delete(self):
        response = self.client.delete(reverse('delete_event_stats'))
        self.assertEqual(response.status_code, 200, msg=vars(response))
        self.assertEqual(EventStats.objects.count(), 0)
