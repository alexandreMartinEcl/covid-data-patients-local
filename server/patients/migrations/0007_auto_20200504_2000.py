# Generated by Django 3.0.5 on 2020-05-04 20:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_auto_20200424_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='detection_ERentree',
            new_name='detection_ER_entree',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='detection_orlEntree',
            new_name='detection_orl_entree',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='detection_ERpremierMardi',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='detection_ERsecondMardi',
        ),
        migrations.AddField(
            model_name='patient',
            name='detections_ER_weekly',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=[], size=None),
        ),
        migrations.AddField(
            model_name='patient',
            name='detections_orl_weekly',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=[], size=None),
        ),
    ]