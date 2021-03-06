# Generated by Django 4.0 on 2021-12-16 13:17

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstats',
            name='click_cost',
            field=models.IntegerField(blank=True, default=Decimal('0'), validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='eventstats',
            name='clicks',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='eventstats',
            name='date_recorded',
            field=models.DateField(default=datetime.datetime(2021, 12, 16, 13, 17, 42, 2801)),
        ),
        migrations.AlterField(
            model_name='eventstats',
            name='views',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
