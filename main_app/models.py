from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEAL_TYPES = (
    ("B", "Breakfast"),
    ("L", "Lunch"),
    ("D", "Dinner"),
)


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=100)
    total_calories = models.IntegerField()
    total_fat = models.IntegerField()
    total_protein = models.IntegerField()
    total_carbs = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("foods_detail", kwargs={"pk": self.id})


class Meal(models.Model):
    date = models.DateField("meal date")
    meal_type = models.CharField(
        max_length=1, choices=MEAL_TYPES, default=MEAL_TYPES[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # foods = models.ManyToManyField(Food)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"meal_id": self.id})

    #
    def __str__(self):
        return f"{self.get_meal_type_display()} on {self.date}"

    # filtered list with recent dates first
    class Meta:
        ordering = ["-date"]
