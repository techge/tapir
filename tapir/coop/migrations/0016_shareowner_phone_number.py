# Generated by Django 3.1.8 on 2021-06-07 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coop", "0015_auto_20210607_1153"),
    ]

    operations = [
        migrations.AddField(
            model_name="shareowner",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="Phone number"
            ),
        ),
    ]
