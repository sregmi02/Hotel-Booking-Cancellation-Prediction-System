# Generated by Django 4.2.5 on 2024-01-08 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0010_remove_booking_special_requests_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='arrival_date',
            field=models.DateField(default=datetime.date(2024, 1, 8)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date(2024, 1, 8)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='departure_date',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
    ]
