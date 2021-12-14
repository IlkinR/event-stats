import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

AVERAGE_PRICE_PER_THOUSAND_VIEWS = 1_000


class EventStats(models.Model):
    date_recorded = models.DateField(default=datetime.datetime.now())
    views = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    clicks = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    click_cost = models.IntegerField(default=Decimal(0), null=True, blank=True,
                                     validators=[MinValueValidator(Decimal(0))])

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
