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
    path(
        "meals/<int:meal_id>/assoc_food/<int:food_id>/",
        views.assoc_food,
        name="assoc_food",
    ),
    path(
        "meals/<int:meal_id>/unassoc_food/<int:food_id>/",
        views.unassoc_food,
        name="unassoc_food",
    ),
    # path("meals/<int:meal_id>/food_form/", views.food_form, name="food_form"),
    # foods route
    path("foods/", views.FoodList.as_view(), name="foods_index"),
    path("foods/foods_search/", views.foods_search, name="foods_search"),
    path("foods/foods_api/", views.foods_API, name="foods_api"),
    path("foods/create/", views.FoodCreate.as_view(), name="foods_create"),
    # path("foods/foods_form/", views.foods_form, name="foods_form"),
    path("foods/<int:pk>/update/", views.FoodUpdate.as_view(), name="food_update"),
    path("foods/<int:pk>/delete/", views.FoodDelete.as_view(), name="food_delete"),
    # accounts route
    path("accounts/signup/", views.signup, name="signup"),
]
