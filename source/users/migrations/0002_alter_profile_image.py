# Generated by Django 4.1.2 on 2022-11-10 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(null=True, upload_to="profile_pics"),
        ),
    ]
