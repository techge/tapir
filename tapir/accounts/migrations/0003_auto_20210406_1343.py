# Generated by Django 3.1.7 on 2021-04-06 13:43

from django.db import migrations, models
import ldapdb.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_auto_20210406_1339"),
    ]

    operations = [
        migrations.AddField(
            model_name="tapiruser",
            name="birthdate",
            field=models.DateField(blank=True, null=True, verbose_name="Birthdate"),
        ),
    ]