from django.db import models
from django.contrib.auth.models import User


class MenuCategory(models.Model):
    name = models.CharField(max_length=50)
    price_info = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="red-600")

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DishOption(models.Model):
    dish_subtype = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='options1')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    event_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event_date}"


class MenuSelection(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='selections')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    option = models.ForeignKey(DishOption, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.dish.name