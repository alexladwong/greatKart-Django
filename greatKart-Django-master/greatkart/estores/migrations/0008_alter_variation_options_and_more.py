# Generated by Django 5.0.1 on 2024-01-14 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("estores", "0007_alter_variation_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="variation",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="variation",
            name="estores_var_created_72916b_idx",
        ),
    ]