# Generated by Django 4.2.5 on 2023-10-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kswap", "0003_booking_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="address",
            field=models.TextField(max_length=20),
        ),
    ]
