# Generated by Django 5.0.1 on 2024-01-14 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estores", "0003_alter_products_product_name_alter_products_slug"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="products",
            options={
                "ordering": ["-created_date"],
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
        migrations.CreateModel(
            name="Variations",
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
                    "variation_category",
                    models.CharField(
                        choices=[("color", "color"), ("size", "size")], max_length=100
                    ),
                ),
                ("variation_value", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estores.products",
                    ),
                ),
            ],
        ),
    ]