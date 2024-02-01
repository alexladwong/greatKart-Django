# Generated by Django 4.1.5 on 2024-01-31 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("estores", "0012_reviewrating"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductGallery",
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
                    "image",
                    models.ImageField(max_length=255, upload_to="etores/products"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estores.products",
                    ),
                ),
            ],
        ),
    ]