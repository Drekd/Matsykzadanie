from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class MuscleGroup(models.Model):
    name = models.CharField(max_length=50)
    body_part = models.CharField(max_length=50)

    class Meta:
        db_table = 'muscle_groups'


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    muscle_groups = models.ForeignKey(
        MuscleGroup, on_delete=models.CASCADE, db_column='muscle_groups_id'
    )
    date = models.DateTimeField()

    class Meta:
        db_table = 'workouts'


class WorkoutStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    muscle_group = models.CharField(max_length=100)
    last_date = models.DateTimeField(null=True, blank=True)
    total = models.IntegerField(default=0)

    class Meta:
        db_table = 'workout_stats'