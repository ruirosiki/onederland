from django.forms import ModelForm
from .models import Foods

class FoodForm(ModelForm):
    class Meta:
        model = Foods
        fields = ['name', 'total_calories','total_fat','total_protein', 'total_carbs']