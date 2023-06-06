from django.forms import ModelForm
from .models import Food


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ["name", "total_calories", "total_fat", "total_protein", "total_carbs"]
