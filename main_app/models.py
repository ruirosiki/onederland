from django.db import models
from django.urls import reverse
from datetime import date

MEAL_TYPES = (
    ("B", "Breakfast"),
    ("L", "Lunch"),
    ("D", "Dinner"),
)


# Create your models here.
class Meal(models.Model):
    date = models.DateField("meal date")
    meal_type = models.CharField(
        max_length=1, choices=MEAL_TYPES, default=MEAL_TYPES[0][0]
    )

    def get_absolute_url(self):
        return reverse("detail", kwargs={"meal_id": self.id})

    #
    def __str__(self):
        return f"{self.get_meal_type_display()} on {self.date}"

    # filtered list with recent dates first
    class Meta:
        ordering = ["-date"]
