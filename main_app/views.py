from django.shortcuts import render, redirect, reverse
from .models import Meal, Food
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json
from .forms import FoodForm
from django.contrib.auth.decorators import login_required

# API - Calorie Ninja


# Create your views here.
def foods_API(request):
    api_url = "https://api.calorieninjas.com/v1/nutrition?query="
    query = request.GET.get("query")
    response = requests.get(
        api_url + str(query),
        headers={"X-Api-Key": "WckbYIY9LQLe8m72V8rEYw==YCE4Hjwib4uDUhdI"},
    )
    data = response.json()
    item_data = data["items"]
    stats = item_data[0]
    filtered_stats = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    wanted_stats = [
        "name",
        "calories",
        "fat_total_g",
        "protein_g",
        "carbohydrates_total_g",
    ]
    filtered_data = filtered_stats(stats, wanted_stats)
    print("this is filtered data", filtered_data)
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    context = {"data": filtered_data}
    return redirect(request, "foods_create", context)


# home view/controller function


def home(request):
    return render(request, "home.html")


# about view/controller function
def about(request):
    return render(request, "about.html")


# meals view/controller function
@login_required
def meals_index(request):
    meals = Meal.objects.filter(user=request.user)
    return render(request, "meals/index.html", {"meals": meals})


@login_required
def meals_details(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    id_list = meal.foods.all().values_list("id")
    foods = Food.objects.exclude(id__in=id_list)
    return render(request, "meals/detail.html", {"meal": meal, "foods": foods})


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


def foods_search(request):
    return render(request, "main_app/food_search.html")


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


# def foods_form(request):
#     return render(request, "foods_create")


@login_required
def assoc_food(request, meal_id, food_id):
    Meal.objects.get(id=meal_id).foods.add(food_id)
    return redirect("detail", meal_id=meal_id)


@login_required
def unassoc_food(request, meal_id, food_id):
    Meal.objects.get(id=meal_id).foods.remove(food_id)
    return redirect("detail", meal_id=meal_id)


# Food Views
class FoodList(LoginRequiredMixin, ListView):
    model = Food


class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food
    fields = "__all__"
    print("success 1")

    def form_valid(self, form):
        form.instance.user = self.request.user
        print("success")
        return super().form_valid(form)


class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    fields = ["total_calories", "total_fat", "total_protein", "total_carbs"]


class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = "/foods"


# def food_create(request, self, form):
#     food = request.session.GET("created_food")
#     form.instance.user = self.request.food
#     return food_create(form)
