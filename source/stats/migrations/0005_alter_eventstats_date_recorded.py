# Generated by Django 4.0 on 2021-12-16 13:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_alter_eventstats_date_recorded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstats',
            name='date_recorded',
            field=models.DateField(default=datetime.datetime(2021, 12, 16, 13, 18, 38, 877490, tzinfo=utc)),
        ),
    ]
