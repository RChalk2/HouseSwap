# Generated by Django 4.2.5 on 2023-10-14 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Kashrut",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter a kashrut organisation", max_length=200
                    ),
                ),
            ],
            options={"ordering": ["name"],},
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("city", models.CharField(max_length=20)),
                ("postcode", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("no_of_rooms", models.PositiveIntegerField()),
                ("estimated_value", models.FloatField()),
                ("property_type", models.CharField(max_length=50)),
                ("amenities", models.TextField()),
                ("pet_friendly", models.BooleanField()),
                ("accessibility_features", models.TextField()),
                ("proximity_to_public_transport", models.PositiveIntegerField()),
                ("nearby_attractions", models.TextField()),
                ("succah", models.BooleanField()),
                ("passover_kitchen", models.BooleanField()),
                ("max_occupancy", models.PositiveIntegerField()),
                ("smoking_allowed", models.BooleanField()),
                ("home_description", models.TextField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telno_mobile", models.CharField(max_length=15)),
                ("rabbi", models.CharField(max_length=100)),
                (
                    "kashrut",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="kswap.kashrut",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="images/")),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="kswap.property"
                    ),
                ),
            ],
        ),
    ]