from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
import requests
import json
from .forms import DailyLogFoodForm, DailyLogExerciseForm
from .models import Food, DailyLogExercise, Exercise, DailyLog, DailyLogFood
from my_movie_club.settings import api_key
from datetime import datetime, timedelta, date
from django.db.models import Sum, F, FloatField

today = date.today()


class CounterHomeView(View):

    def get(self, request):
        return render(request, 'home.html', {'query': 'Enter a valid query'})

    def post(self, request):
        query = request.POST.get('query')
        food = Food.objects.filter(name=query).first()
        if not food:
            try:
                api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
                api_request = requests.get(api_url + query, headers={'X-Api-Key': api_key})
                if json.loads(api_request.content):
                    api = json.loads(api_request.content)
                    api_food = api[0]
                    food = Food.objects.create(
                        name=query,
                        calories=api_food.get('calories'),
                        serving_size_g=api_food.get('serving_size_g'),
                        fat_total_g=api_food.get('fat_total_g'),
                        fat_saturated_g=api_food.get('fat_saturated_g'),
                        protein_g=api_food.get('protein_g'),
                        sodium_mg=api_food.get('sodium_mg'),
                        potassium_mg=api_food.get('potassium_mg'),
                        cholesterol_mg=api_food.get('cholesterol_mg'),
                        carbohydrates_total_g=api_food.get('carbohydrates_total_g'),
                        fiber_g=api_food.get('fiber_g'),
                        sugar_g=api_food.get('sugar_g'),
                    )
                    food.save()
                else:
                    messages.error(request, 'Food not found in the API.')
                    return redirect('counter')
            except:
                messages.error(request, 'Error occurred while fetching food details from the API.')
                # return redirect('counter')
        else:
            api = Food.objects.filter(name=query)
        return render(request, 'home.html', {'api': api})


class AddFoodItemView(View):

    def get(self, request):
        form = DailyLogFoodForm()
        foods = Food.objects.all()
        return render(request, 'add_food_item.html', {'form': form, 'foods': foods})

    def post(self, request):
        form = DailyLogFoodForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            daily_log = DailyLog.objects.filter(profile=request.user.profile, date=date).first()
            food_name = request.POST.get('name')
            food = Food.objects.filter(name=food_name).first()
            if not food:
                api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
                api_request = requests.get(api_url + food_name, headers={'X-Api-Key': api_key})
                try:
                    if json.loads(api_request.content):
                        api_food = json.loads(api_request.content)[0]
                        food = Food.objects.create(
                            name=food_name,
                            calories=api_food.get('calories'),
                            serving_size_g=api_food.get('serving_size_g'),
                            fat_total_g=api_food.get('fat_total_g'),
                            fat_saturated_g=api_food.get('fat_saturated_g'),
                            protein_g=api_food.get('protein_g'),
                            sodium_mg=api_food.get('sodium_mg'),
                            potassium_mg=api_food.get('potassium_mg'),
                            cholesterol_mg=api_food.get('cholesterol_mg'),
                            carbohydrates_total_g=api_food.get('carbohydrates_total_g'),
                            fiber_g=api_food.get('fiber_g'),
                            sugar_g=api_food.get('sugar_g'),
                        )
                    else:
                        messages.error(request, 'Food not found in the API.')
                        return redirect('add_food')
                except:
                    messages.error(request, 'Error occurred while fetching food details from the API.')
                    return redirect('add_food')

            if daily_log:
                DailyLogFood.objects.create(
                    daily_log=daily_log,
                    food=food,
                    description=request.POST.get('description'),
                    quantity=request.POST.get('quantity'))

                daily_log.intake_calories += (food.calories * float(request.POST.get('quantity')) / 100)
                daily_log.save()

            else:
                daily_log = DailyLog.objects.create(
                    profile=request.user.profile,
                    date=date,
                    intake_calories=(food.calories * float(request.POST.get('quantity')) / 100),
                )
                DailyLogFood.objects.create(
                    daily_log=daily_log,
                    food=food,
                    description=request.POST.get('description'),
                    quantity=request.POST.get('quantity'))

            messages.success(request, 'Food entry added successfully.')
            return redirect('food_log')
        else:
            foods = Food.objects.all()
            messages.error(request, 'Invalid form submission. Please correct the errors.')
            return render(request, 'add_food_item.html', {'form': form, 'foods': foods, 'today': today})


class FoodLogView(View):

    def get(self, request):
        food_entries = DailyLogFood.objects.filter(daily_log__profile__user=request.user).order_by(
            '-daily_log__date')
        return render(request, 'food_log.html', {'food_entries': food_entries})


class DeleteFoodEntryView(View):
    def post(self, request, food_entry_id):
        food_entry = get_object_or_404(DailyLogFood, id=food_entry_id)
        food_entry.delete()
        messages.success(request, 'Food entry deleted successfully.')
        return redirect('food_log')


class UpdateFoodEntryView(View):
    def get(self, request, food_entry_id):
        food_entry = get_object_or_404(DailyLogFood, id=food_entry_id)
        form = DailyLogFoodForm(instance=food_entry)
        foods = Food.objects.all()
        return render(request, 'add_food_item.html', {'form': form, 'foods': foods, 'food_entry': food_entry})

    def post(self, request, food_entry_id):
        food_entry = get_object_or_404(DailyLogFood, id=food_entry_id)
        form = DailyLogFoodForm(request.POST, instance=food_entry)
        foods = Food.objects.all()
        if form.is_valid():
            form.save()
            messages.success(request, 'Food entry updated successfully.')
            return redirect('food_log')
        return render(request, 'add_food_item.html', {'form': form, 'foods': foods, 'food_entry': food_entry})


class AddExerciseView(View):
    def get(self, request):
        form = DailyLogExerciseForm()
        return render(request, 'add_exercise.html', {'form': form})

    def post(self, request):
        form = DailyLogExerciseForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            daily_log = DailyLog.objects.filter(profile=request.user.profile, date=date).first()
            activity = request.POST.get('activity')
            # exercise = Exercise.filter(exercise=activity).first()
            duration = int(request.POST.get('duration'))
            user_profile = request.user.profile
            weight = user_profile.weight

            if weight < 50:
                return render(request, 'add_exercise.html', {'error': "Weight must be 50 kg or more."})

            url = "https://api.api-ninjas.com/v1/caloriesburned"

            params = {
                'activity': activity,
                'duration': duration,
                'weight': weight,
            }

            headers = {
                'X-Api-Key': api_key
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            burned_calories = data[0]['total_calories']

            exercise_instance, _ = Exercise.objects.get_or_create(exercise=activity)

            if not daily_log:
                daily_log = DailyLog.objects.create(
                    profile=request.user.profile,
                    date=date,
                    burned_calories=burned_calories)
            else:
                daily_log.burned_calories += float(burned_calories)
                daily_log.save()

            exercise_entry = DailyLogExercise(
                daily_log=daily_log,
                exercise=exercise_instance,
                duration=duration,
                weight=weight,
                burned_calories=burned_calories,
            )
            exercise_entry.save()
            messages.success(request, 'Exercise entry added successfully.')
            return redirect('exercise_log')
        else:
            return render(request, 'add_exercise.html', {'error': 'Error occurred while fetching burned calories.'})


class ExerciseLogView(View):

    def get(self, request):
        exercise_entries = DailyLogExercise.objects.filter(daily_log__profile__user=request.user).order_by(
            '-daily_log__date')
        return render(request, 'exercise_log.html', {'exercise_entries': exercise_entries})


class DeleteExerciseEntryView(View):

    def post(self, request, exercise_entry_id):
        exercise_entry = get_object_or_404(DailyLogExercise, id=exercise_entry_id)
        exercise_entry.delete()
        messages.success(request, 'Exercise entry deleted successfully.')
        return redirect('exercise_log')


class DailyLogView(View):
    def get(self, request):
        daily_logs = DailyLog.objects.filter(profile=request.user.profile).order_by('-date')

        paginator = Paginator(daily_logs, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        selected_date_str = request.GET.get('date')
        try:
            selected_date = datetime.strptime(selected_date_str, '%d-%m-%y').date()
        except (ValueError, TypeError):
            selected_date = None

        food_log_entries = None
        exercise_log_entries = None
        total_intake_calories = 0
        total_burned_calories = 0
        daily_calories = []

        if selected_date:
            food_log_entries = DailyLogFood.objects.filter(daily_log__profile=request.user.profile,
                                                           daily_log__date=selected_date)
            exercise_log_entries = DailyLogExercise.objects.filter(daily_log__profile=request.user.profile,
                                                                   daily_log__date=selected_date)

            total_intake_calories = food_log_entries.aggregate(
                total_intake=Sum(F('food__calories') * F('quantity') / 100,
                                 output_field=FloatField()))['total_intake'] or 0.0
            total_burned_calories = exercise_log_entries.aggregate(total_burned=Sum('burned_calories'))[
                                        'total_burned'] or 0
            selected_week_start = selected_date - timedelta(days=selected_date.weekday())
            daily_calories = []

            for i in range(7):
                selected_day = selected_week_start + timedelta(days=i)
                my_daily_log = DailyLog.objects.filter(profile=request.user.profile, date=selected_day).first()
                if my_daily_log:
                    daily_calories.append(my_daily_log.intake_calories)
                else:
                    daily_calories.append(0)
        username = request.user.username

        context = {
            'daily_logs': daily_logs,
            'selected_date': selected_date_str,
            'food_log_entries': food_log_entries,
            'exercise_log_entries': exercise_log_entries,
            'total_intake_calories': total_intake_calories,
            'total_burned_calories': total_burned_calories,
            'daily_calories': daily_calories,
            'page_obj': page_obj,
            'username': username,
        }
        return render(request, 'daily_log.html', context)


class CreateDailyLogView(View):
    def get(self, request):
        daily_log = DailyLog.objects.filter(profile=request.user.profile, date=today).first()
        if not daily_log:
            DailyLog.objects.create(profile=request.user.profile, date=today)
            messages.info(request, 'New daily log created successfully.')
        else:
            messages.warning(request, 'A daily log already exists for today.')
        return redirect('daily_log')


class DeleteDailyLogView(View):
    def post(self, request, selected_date):
        try:
            selected_date_obj = datetime.strptime(selected_date, '%d-%m-%y').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('daily_log')

        daily_log = get_object_or_404(DailyLog, profile=request.user.profile, date=selected_date_obj)
        daily_log.delete()
        messages.success(request, 'Daily log entry deleted successfully.')
        return redirect('daily_log')
