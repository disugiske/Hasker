# Generated by Django 4.1.2 on 2022-10-24 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hasite", "0023_post_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="posttags",
            name="post_id",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="hasite.post"
            ),
            preserve_default=False,
        ),
    ]