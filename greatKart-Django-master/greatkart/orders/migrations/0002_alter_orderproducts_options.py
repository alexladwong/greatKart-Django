# Generated by Django 5.0.1 on 2024-01-20 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="orderproducts",
            options={
                "verbose_name": "orderProducts",
                "verbose_name_plural": "orderProducts",
            },
        ),
    ]
