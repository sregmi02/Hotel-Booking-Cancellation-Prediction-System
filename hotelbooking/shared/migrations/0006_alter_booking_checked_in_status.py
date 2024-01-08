# Generated by Django 4.2.5 on 2024-01-06 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0005_booking_checked_in_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='checked_in_status',
            field=models.BooleanField(choices=[('True', 'Checked In'), ('False', 'Not Checked In')], null=True),
        ),
    ]
