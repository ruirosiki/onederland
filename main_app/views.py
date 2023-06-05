from django.shortcuts import render, redirect
from .models import Meal

meals = [
    {'mealtype': 'breakfast', 'date': 20230605 }
]


# Create your views here.

# home view/controller function
def home(request):
    return render(request, 'home.html')

# about view/controller function
def about(request):
    return render(request, 'about.html')

# meals view/controller function
def meals_index(request):
    return render(request, 'meals/index.html', {
        'meals': meals
    })