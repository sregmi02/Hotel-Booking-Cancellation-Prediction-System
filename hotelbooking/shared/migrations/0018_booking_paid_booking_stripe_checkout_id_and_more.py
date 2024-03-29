# Generated by Django 4.2.5 on 2024-01-26 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0017_booking_advance_alter_booking_checked_in_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='stripe_checkout_id',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.date(2024, 1, 26)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='checkin_date',
            field=models.DateField(default=datetime.date(2024, 1, 26)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='checkout_date',
            field=models.DateField(default=datetime.date(2024, 1, 27)),
        ),
    ]
