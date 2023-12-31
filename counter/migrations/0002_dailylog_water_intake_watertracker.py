# Generated by Django 4.2.3 on 2023-08-07 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailylog',
            name='water_intake',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='WaterTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intake_ml', models.PositiveIntegerField(default=0)),
                ('daily_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.dailylog')),
            ],
        ),
    ]
