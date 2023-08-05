# Generated by Django 2.1.4 on 2019-01-14 00:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_locator", "0016_auto_20181108_0353")]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectlocator",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.Site",
            ),
        )
    ]
