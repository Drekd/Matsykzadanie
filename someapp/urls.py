from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_all),
    path('users/<int:user_id>/', views.user_detail),

    path('muscle_groups/', views.muscle_groups_all),
    path('muscle_groups/<int:group_id>/', views.muscle_group_detail),

    path('workouts/', views.workouts_all),
    path('workouts/<int:workout_id>/', views.workout_detail),
    path('workouts/date/<str:date>/', views.workouts_by_date),
    path('workouts/user/<int:user_id>/', views.workouts_by_user),
    path('workouts/muscle/<int:group_id>/', views.workouts_by_muscle),

    path('stats/total/<int:user_id>/', views.stats_total),
    path('stats/user/<int:user_id>/', views.stats_by_user),
    path('stats/regularity/', views.stats_regularity),
    path('stats/update/', views.stats_update),
]