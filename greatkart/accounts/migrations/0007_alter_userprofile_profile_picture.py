# Generated by Django 4.1.5 on 2024-01-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_remove_userprofile_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="images/users/"),
        ),
    ]