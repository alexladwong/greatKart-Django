# Generated by Django 4.1.5 on 2024-01-20 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0005_cart_cart_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="cart_name",
        ),
    ]