# Generated by Django 5.0.1 on 2024-01-22 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_rename_phone_order_phone_number_alter_order_email_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproducts",
            name="color",
        ),
        migrations.RemoveField(
            model_name="orderproducts",
            name="size",
        ),
    ]