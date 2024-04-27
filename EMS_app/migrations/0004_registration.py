# Generated by Django 5.0.2 on 2024-04-04 23:25

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EMS_app", "0003_alter_organizer_phone_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Registration",
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
                    "registration_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("registered", "Registered"),
                            ("unregistered", "Unregistered"),
                        ],
                        default="registered",
                        max_length=12,
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="registrations",
                        to="EMS_app.event",
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="registrations",
                        to="EMS_app.participant",
                    ),
                ),
            ],
        ),
    ]
