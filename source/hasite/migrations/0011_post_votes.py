# Generated by Django 4.1.2 on 2022-10-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hasite", "0010_postcomments"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="votes",
            field=models.IntegerField(default=0),
        ),
    ]
