# Generated by Django 4.2.5 on 2024-01-03 03:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0003_booking_dynamic_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='arrival_date',
            field=models.DateField(default=datetime.date(2024, 1, 3)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date(2024, 1, 3)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='departure_date',
            field=models.DateField(default=datetime.date(2024, 1, 3)),
        ),
    ]
