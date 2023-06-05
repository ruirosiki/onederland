from django.shortcuts import render, redirect
from .models import Meal
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

# home view/controller function
def home(request):
    return render(request, 'home.html')

# about view/controller function
def about(request):
    return render(request, 'about.html')

# meals view/controller function
def meals_index(request):
    meals = Meal.objects.all()
    return render(request, 'meals/index.html', {
        'meals': meals
    })

def meals_details(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    return render(request, 'meals/detail.html', {
        'meal':meal
    })


class MealCreate(LoginRequiredMixin, CreateView):
    model = Meal
    fields = ['date', 'meal_type']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class MealUpdate(LoginRequiredMixin, UpdateView):
    model = Meal
    fields = ['date', 'meal_type']

class MealDelete(LoginRequiredMixin, DeleteView):
    model = Meal
    success_url = '/meals/'


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

