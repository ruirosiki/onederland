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
from django.db.models import Sum
from datetime import date

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
        print("success")
    else:
        print("Error:", response.status_code, response.text)

    # context = {"data": filtered_data}
    request.session["filtered_data"] = filtered_data
    print(filtered_data)
    return redirect("foods_create")
    # redirect_url = "foods/create/"
    # for key, value in filtered_data.items():
    #     redirect_url += f"{key} = {value}&"
    # return redirect(redirect_url)


# home view/controller function


def home(request):
    today = date.today()
    meal_entries = Meal.objects.filter(date = today)
    total_calories = meal_entries.aggregate(total=Sum('foods__total_calories'),)['total']
    total_fat = meal_entries.aggregate(total=Sum('foods__total_fat'),)['total']
    total_protein = meal_entries.aggregate(total=Sum('foods__total_protein'),)['total']
    total_carbs = meal_entries.aggregate(total=Sum('foods__total_carbs'),)['total']

    meal_entries_B = Meal.objects.filter(date = today, meal_type = 'B')
    food_name = Meal.foods.values_list('name') 
    food_name = list(food_name)
    print(food_name)
    total_calories_B = meal_entries_B.aggregate(total=Sum('foods__total_calories'),)['total']
    total_fat_B = meal_entries_B.aggregate(total=Sum('foods__total_fat'),)['total']
    total_protein_B = meal_entries_B.aggregate(total=Sum('foods__total_protein'),)['total']
    total_carbs_B = meal_entries_B.aggregate(total=Sum('foods__total_carbs'),)['total']

    meal_entries_L = Meal.objects.filter(date = today, meal_type = 'L')
    total_calories_L = meal_entries_L.aggregate(total=Sum('foods__total_calories'),)['total']
    total_fat_L = meal_entries_L.aggregate(total=Sum('foods__total_fat'),)['total']
    total_protein_L = meal_entries_L.aggregate(total=Sum('foods__total_protein'),)['total']
    total_carbs_L = meal_entries_L.aggregate(total=Sum('foods__total_carbs'),)['total']

    meal_entries_D = Meal.objects.filter(date = today, meal_type = 'D')
    total_calories_D = meal_entries_D.aggregate(total=Sum('foods__total_calories'),)['total']
    total_fat_D = meal_entries_D.aggregate(total=Sum('foods__total_fat'),)['total']
    total_protein_D = meal_entries_D.aggregate(total=Sum('foods__total_protein'),)['total']
    total_carbs_D = meal_entries_D.aggregate(total=Sum('foods__total_carbs'),)['total']

    context = {'total_calories_B': total_calories_B, 'total_fat_B':total_fat_B, 'total_protein_B':total_protein_B, 'total_carbs_B':total_carbs_B,'total_calories_L': total_calories_L, 'total_fat_L':total_fat_L, 'total_protein_L':total_protein_L, 'total_carbs_L':total_carbs_L,'total_calories_D': total_calories_D, 'total_fat_D':total_fat_D, 'total_protein_D':total_protein_D, 'total_carbs_D':total_carbs_D, 'today':today, 'meal_entries_B':meal_entries_B, 'meal_entries_L':meal_entries_L, 'meal_entries_D':meal_entries_D, 'total_calories': total_calories, 'total_fat':total_fat, 'total_protein':total_protein, 'total_carbs':total_carbs, 'meal_entries':meal_entries, 'food_name':food_name}
    return render(request, "home.html", context)


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

    def get_initial(self):
        initial = super().get_initial()
        filtered_data = self.request.session.get("filtered_data", {})
        initial["name"] = filtered_data.get("name", "")
        initial["total_calories"] = int(filtered_data.get("calories", ""))
        initial["total_fat"] = int(filtered_data.get("fat_total_g", ""))
        initial["total_carbs"] = int(filtered_data.get("carbohydrates_total_g", ""))
        initial["total_protein"] = int(filtered_data.get("protein_g", ""))
        return initial

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
