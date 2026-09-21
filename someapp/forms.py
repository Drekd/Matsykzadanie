from django import forms
from .models import User, MuscleGroup, Workout


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']


class MuscleGroupForm(forms.ModelForm):
    class Meta:
        model = MuscleGroup
        fields = ['name', 'body_part']


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['user', 'muscle_groups', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }