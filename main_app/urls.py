from django.urls import path
from . import views



urlpatterns = [
    # home route
    path('', views.home, name='home'),
    
    # about route
    path('about/', views.about, name='about'),

    # meals route
    path('meals/', views.meals_index, name='meals_index'),
    path('meals/<int:meal_id>/', views.meals_details, name='meals_details'),
    path('meals/create/', views.MealCreate.as_view(), name='meals_create'),
    
    # accounts route
    path('accounts/signup/', views.signup, name='signup'),
]