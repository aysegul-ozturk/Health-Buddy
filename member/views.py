from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import UserRegisterForm, ProfileForm
from .models import Profile

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'member/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')
            return render(request, 'member/register.html', {'form': form})


def calculate_bmi(weight, height):
    height_in_meters = height / 100  # Convert cm to m
    bmi = weight / (height_in_meters * height_in_meters)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


class ProfileView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        my_profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=my_profile)
        bmi = calculate_bmi(my_profile.weight, my_profile.height)
        bmi_category = get_bmi_category(bmi)
        return render(request, 'member/profile.html', {'form': form, 'bmi': bmi, 'bmi_category': bmi_category})

    def post(self, request):
        my_profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, instance=my_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')
            return render(request, 'member/profile.html', {'form': form})

