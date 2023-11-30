# Generated by Django 4.2.3 on 2023-08-02 07:50

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0004_alter_profile_height_alter_profile_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('intake_calories', models.IntegerField(default=0)),
                ('burned_calories', models.FloatField(default=0)),
                ('profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.FloatField()),
                ('serving_size_g', models.FloatField()),
                ('fat_total_g', models.FloatField()),
                ('fat_saturated_g', models.FloatField()),
                ('protein_g', models.FloatField()),
                ('sodium_mg', models.FloatField()),
                ('potassium_mg', models.FloatField()),
                ('cholesterol_mg', models.FloatField()),
                ('carbohydrates_total_g', models.FloatField()),
                ('fiber_g', models.FloatField()),
                ('sugar_g', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyLogFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField()),
                ('quantity', models.FloatField()),
                ('daily_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.dailylog')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.food')),
            ],
        ),
        migrations.CreateModel(
            name='DailyLogExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('burned_calories', models.FloatField()),
                ('daily_log', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='counter.dailylog')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counter.exercise')),
            ],
        ),
    ]
