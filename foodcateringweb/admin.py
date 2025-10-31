from django.contrib import admin
from .models import MenuCategory, Dish, DishOption, Order, MenuSelection

class MenuSelectionInline(admin.TabularInline):
    model = MenuSelection
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event_date', 'created_at')
    list_filter = ('event_date', 'user')
    inlines = [MenuSelectionInline]

admin.site.register(MenuCategory)
admin.site.register(Dish)
admin.site.register(DishOption)
admin.site.register(Order, OrderAdmin)