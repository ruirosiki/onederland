from django.shortcuts import render, redirect
from .models import Meal
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm


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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

