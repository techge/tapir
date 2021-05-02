# Generated by Django 3.1.7 on 2021-04-11 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_auto_20210411_0559"),
        ("odoo", "0001_initial"),
        ("coop", "0002_auto_20210406_1431"),
    ]

    operations = [
        migrations.AddField(
            model_name="draftuser",
            name="coop_share_invoice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="finance.invoice",
            ),
        ),
        migrations.AddField(
            model_name="draftuser",
            name="odoo_partner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="odoo.odoopartner",
            ),
        ),
        migrations.AlterField(
            model_name="draftuser",
            name="num_shares",
            field=models.IntegerField(
                default=1, editable=False, verbose_name="Number of Shares"
            ),
        ),
    ]