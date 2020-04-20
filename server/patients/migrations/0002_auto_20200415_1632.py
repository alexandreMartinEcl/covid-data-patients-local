# Generated by Django 3.0.5 on 2020-04-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='allergies',
            field=models.TextField(blank=True, default='["Non indiqué"]', help_text='["pollen"]', null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='antecedents',
            field=models.TextField(blank=True, default='{"NonIndique": ""}', help_text='json {"Cardio": "note"}̀', null=True),
        ),
    ]