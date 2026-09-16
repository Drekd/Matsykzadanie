from django.urls import path
from . import views

urlpatterns = [
  
    path('users/', views.UserListView.as_view()),
    path('users/<int:user_id>/', views.UserDetailView.as_view()),

    path('muscle_groups/', views.MuscleGroupListView.as_view()),
    path('muscle_groups/<int:group_id>/', views.MuscleGroupDetailView.as_view()),

    path('workouts/', views.WorkoutListView.as_view()),
    path('workouts/<int:workout_id>/', views.WorkoutDetailView.as_view()),
    path('workouts/date/<str:date>/', views.WorkoutByDateView.as_view()),
    path('workouts/user/<int:user_id>/', views.WorkoutByUserView.as_view()),
    path('workouts/muscle/<int:group_id>/', views.WorkoutByMuscleView.as_view()),

    path('stats/total/<int:user_id>/', views.StatsTotalView.as_view()),
    path('stats/user/<int:user_id>/', views.StatsByUserView.as_view()),
    path('stats/regularity/', views.StatsRegularityView.as_view()),
    path('stats/update/', views.StatsUpdateView.as_view()),
]