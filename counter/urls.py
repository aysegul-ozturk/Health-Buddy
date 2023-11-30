from django.urls import path
from .views import CounterHomeView, AddFoodItemView, FoodLogView, DeleteFoodEntryView, \
    AddExerciseView, ExerciseLogView, DeleteExerciseEntryView, DailyLogView, DeleteDailyLogView, UpdateFoodEntryView, CreateDailyLogView

urlpatterns = [
    path('counter', CounterHomeView.as_view(), name='counter_home'),
    path('counter/add/', AddFoodItemView.as_view(), name='food'),
    path('food_log/', FoodLogView.as_view(), name='food_log'),
    path('food_log/delete/<int:food_entry_id>/', FoodLogView.as_view(), name='delete_food_entry'),
    path('update_food_entry/<int:food_entry_id>/', UpdateFoodEntryView.as_view(), name='update_food_entry'),
    path('exercise_log/', ExerciseLogView.as_view(), name='exercise_log'),
    path('exercise_log/delete/<int:exercise_entry_id>/', DeleteExerciseEntryView.as_view(), name='delete_exercise_entry'),
    path('add_exercise/', AddExerciseView.as_view(), name='add_exercise'),
    path('daily_log/', DailyLogView.as_view(), name='daily_log'),
    path('delete_daily_log/<str:selected_date>/', DeleteDailyLogView.as_view(), name='delete_daily_log'),
    path('create_empty_daily_log/', CreateDailyLogView.as_view(), name='create_empty_daily_log'),
]

