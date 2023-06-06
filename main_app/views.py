from django.shortcuts import render, redirect, reverse
from .models import Meal, Food
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json
from .forms import FoodForm

# API - Calorie Ninja


# Create your views here.
def add_food(request, meal_id):
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    query = request.POST.get("query")
    response = requests.get(
        api_url + query,
        headers={"X-Api-Key": "WckbYIY9LQLe8m72V8rEYw==YCE4Hjwib4uDUhdI"},
    )
    data = response.json()
    item_data = data["items"]
    stats = item_data[0]
    print("this is stats.items()", stats.items())
    print("this is food.filtered", Food.filtered_stats)
    filtered_data = dict(filter(Food.filtered_stats, stats))
    print("this is filtered data", filtered_data)
    # for x in stats:
    #     print("this is x:", x)
    #     # print("this is y:", y)
    #     if x == "name":
    #         filtered_data.append(x[0])
    #     return filtered_data
    if response.status_code == requests.codes.ok:
        # print(response.text)
        form = FoodForm(request.POST)
        if form.is_valid():
            new_food = form.save(commit=False)
            new_food.meal_id = meal_id
            new_food.save()
    else:
        print("Error:", response.status_code, response.text)
    return redirect("detail", meal_id=meal_id)


# home view/controller function


def home(request):
    return render(request, "home.html")


# about view/controller function
def about(request):
    return render(request, "about.html")


# meals view/controller function
def meals_index(request):
    meals = Meal.objects.filter(user=request.user)
    return render(request, "meals/index.html", {"meals": meals})


def meals_details(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    return render(request, "meals/detail.html", {"meal": meal})


# def food_form


def food_form(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    food_form = FoodForm()
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    if request.method == "POST":
        query = request.POST.get("query")
        return query

    response = requests.get(
        api_url + query,
        headers={"X-Api-Key": "WckbYIY9LQLe8m72V8rEYw==YCE4Hjwib4uDUhdI"},
    )

    data = response.json()
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    return render(
        request, "main_app/food_form.html", {"meal": meal, "food_form": food_form}
    )


def on_click(request):
    button_clicked = True


class MealCreate(LoginRequiredMixin, CreateView):
    model = Meal
    fields = ["date", "meal_type"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealUpdate(LoginRequiredMixin, UpdateView):
    model = Meal
    fields = ["date", "meal_type"]


class MealDelete(LoginRequiredMixin, DeleteView):
    model = Meal
    success_url = "/meals/"


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
