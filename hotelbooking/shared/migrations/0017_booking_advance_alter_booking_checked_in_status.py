# Generated by Django 4.2.5 on 2024-01-12 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0016_alter_booking_booking_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='advance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='checked_in_status',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
