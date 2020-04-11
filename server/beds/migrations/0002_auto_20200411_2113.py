# Generated by Django 3.0.5 on 2020-04-11 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beds', '0001_initial'),
        ('users', '0001_initial'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitstay',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_stays_created', to='users.UserProfile'),
        ),
        migrations.AddField(
            model_name='unitstay',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='unit',
            name='reanimation_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beds.ReanimationService'),
        ),
        migrations.AddField(
            model_name='reanimationservice',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Hospital'),
        ),
        migrations.AddField(
            model_name='bed',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='beds.Unit'),
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('name', 'reanimation_service')},
        ),
        migrations.AlterUniqueTogether(
            name='reanimationservice',
            unique_together={('name', 'hospital')},
        ),
        migrations.AlterUniqueTogether(
            name='bed',
            unique_together={('unit', 'unit_index')},
        ),
    ]
