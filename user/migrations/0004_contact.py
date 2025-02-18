# Generated by Django 5.0.2 on 2024-05-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_user_phone_alter_user_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                    "firstname",
                    models.CharField(max_length=30, verbose_name="first name"),
                ),
                ("lastname", models.CharField(max_length=30, verbose_name="last name")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("message", models.TextField(max_length=500, verbose_name="message")),
            ],
        ),
    ]
