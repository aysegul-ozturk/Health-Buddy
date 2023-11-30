from django.db import models
from ckeditor.fields import RichTextField

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    serving_size_g = models.FloatField()
    fat_total_g = models.FloatField()
    fat_saturated_g = models.FloatField()
    protein_g = models.FloatField()
    sodium_mg = models.FloatField()
    potassium_mg = models.FloatField()
    cholesterol_mg = models.FloatField()
    carbohydrates_total_g = models.FloatField()
    fiber_g = models.FloatField()
    sugar_g = models.FloatField()

    def __str__(self):
        return self.name

class Exercise(models.Model):
    exercise = models.CharField(max_length=100)

    def __str__(self):
        return self.exercise

class DailyLog(models.Model):
    profile = models.ForeignKey(to='member.Profile', on_delete=models.CASCADE, default=None, null=True)
    date = models.DateField()
    intake_calories = models.IntegerField(default=0)
    burned_calories = models.FloatField(default=0)

class DailyLogExercise(models.Model):
    daily_log = models.ForeignKey(to=DailyLog, on_delete=models.CASCADE, default=None, null=True)
    exercise = models.ForeignKey(to=Exercise, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    burned_calories = models.FloatField()

class DailyLogFood(models.Model):
    daily_log = models.ForeignKey(to=DailyLog, on_delete=models.CASCADE)
    food = models.ForeignKey(to=Food, on_delete=models.CASCADE)
    description = RichTextField()
    quantity = models.FloatField()

class WaterTracker(models.Model):
    daily_log = models.ForeignKey(to=DailyLog, on_delete=models.CASCADE)
    intake_ml = models.PositiveIntegerField(default=0)

