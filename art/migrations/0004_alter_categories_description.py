# Generated by Django 5.0.2 on 2024-04-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("art", "0003_categories_art_catogories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categories",
            name="description",
            field=models.TextField(null=True),
        ),
    ]
