# Generated by Django 3.0.5 on 2020-04-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_auto_20200419_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='hospitalisation_cause',
            field=models.TextField(blank=True, null=True),
        ),
    ]
