from django import forms
from .models import DailyLogFood, DailyLogExercise
from ckeditor.widgets import CKEditorWidget

class DailyLogFoodForm(forms.ModelForm):
    date = forms.DateField()
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = DailyLogFood
        fields = ['description', 'quantity']


class DailyLogExerciseForm(forms.ModelForm):
    date = forms.DateField()

    class Meta:
        model = DailyLogExercise
        fields = ['duration']