# Generated by Django 4.2.5 on 2024-01-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0006_alter_booking_checked_in_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='checked_in_status',
            field=models.CharField(choices=[('True', 'Checked In'), ('False', 'Not Checked In')], max_length=20, null=True),
        ),
    ]
