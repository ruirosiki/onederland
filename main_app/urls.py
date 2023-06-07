from django.urls import path
from . import views


urlpatterns = [
    # home route
    path("", views.home, name="home"),
    # about route
    path("about/", views.about, name="about"),
    # meals route
    path("meals/", views.meals_index, name="meals_index"),
    path("meals/<int:meal_id>/", views.meals_details, name="detail"),
    path("meals/create/", views.MealCreate.as_view(), name="meals_create"),
    path("meals/<int:pk>/update/", views.MealUpdate.as_view(), name="meals_update"),
    path("meals/<int:pk>/delete/", views.MealDelete.as_view(), name="meals_delete"),
    # path("meals/<int:meal_id>/food_form/", views.food_form, name="food_form"),
    path("foods/search_food/", views.search_food, name="search_food"),
    # foods route
    path("foods/", views.FoodList.as_view(), name="foods_index"),
    path("foods/create/", views.FoodCreate.as_view(), name="foods_create"),
    # accounts route
    path("accounts/signup/", views.signup, name="signup"),
]
