import datetime
from decimal import Decimal

from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

AVERAGE_PRICE_PER_THOUSAND_VIEWS = 1_000


class EventStatsQuerySet(models.QuerySet):
    def get_sorted_event_stats(self, field_to_sort, start_date, last_date):
        date_query_mask = Q(date_recorded__gte=start_date) & Q(date_recorded__lte=last_date)
        return self.filter(date_query_mask).order_by('date_recorded', field_to_sort)


class EventStats(models.Model):
    date_recorded = models.DateField(default=timezone.now())
    views = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0)])
    clicks = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0)])
    click_cost = models.IntegerField(default=Decimal(0), blank=True, validators=[MinValueValidator(Decimal(0))])

    objects = EventStatsQuerySet.as_manager()

    class Meta:
        verbose_name = 'Event statistics'
        verbose_name_plural = 'Event statistics'

    def __str__(self):
        return f'EventStats(date={self.date_recorded}, views={self.views})'

    @property
    def cpc(self):
        try:
            cpc = Decimal(self.click_cost / self.clicks)
            return round(Decimal(cpc), 2)
        except ZeroDivisionError:
            return None

    @property
    def cpm(self):
        try:
            cpm = (self.click_cost / self.views) * AVERAGE_PRICE_PER_THOUSAND_VIEWS
            return round(Decimal(cpm), 2)
        except ZeroDivisionError:
            return None
