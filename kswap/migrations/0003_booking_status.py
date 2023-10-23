# Generated by Django 4.2.5 on 2023-10-22 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kswap", "0002_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
