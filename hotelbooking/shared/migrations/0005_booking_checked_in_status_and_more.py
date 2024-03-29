# Generated by Django 4.2.5 on 2024-01-06 04:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0004_alter_booking_arrival_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='checked_in_status',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_bookings_cancelled',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_bookings_not_cancelled',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='booking',
            name='arrival_date',
            field=models.DateField(default=datetime.date(2024, 1, 6)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date(2024, 1, 6)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='departure_date',
            field=models.DateField(default=datetime.date(2024, 1, 7)),
        ),
    ]
