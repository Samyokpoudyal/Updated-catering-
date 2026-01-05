from django.db import models
from django.contrib.auth.models import User

class MenuCategory(models.Model):
    SERVICE_CHOICES = [
        ('party_pack', 'Party Pack'),
        ('lunchbox', 'Lunchbox'),
        ('catering', 'Catering'),
    ]
    
    service_type = models.CharField(
        max_length=20, 
        choices=SERVICE_CHOICES, 
        default='party_pack'
    )
    name = models.CharField(max_length=50)
    price_info = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="red-600")

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.name}"


class Dish(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='subitems')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'In Process'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    event_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New status field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )

    # Location fields
    delivery_address = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.event_date}"


class MenuSelection(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='selections')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    subitems = models.ManyToManyField(SubItem, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.dish.name
