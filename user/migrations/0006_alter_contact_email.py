# Generated by Django 5.0.2 on 2024-05-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_contact_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="email address"),
        ),
    ]
