# Generated by Django 5.0.1 on 2024-01-11 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("estores", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="products",
            options={"verbose_name": "product", "verbose_name_plural": "products"},
        ),
    ]
