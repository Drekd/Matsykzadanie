from django.contrib import admin
from .models import User, MuscleGroup, Workout, WorkoutStats

admin.site.register(User)
admin.site.register(MuscleGroup)
admin.site.register(Workout)
admin.site.register(WorkoutStats)