from django.contrib import admin
from .models import MenuCategory, Dish, SubItem, Order, MenuSelection


# ===============================
# INLINE: MenuSelection (Order)
# ===============================
class MenuSelectionInline(admin.TabularInline):
    model = MenuSelection
    extra = 0
    can_delete = False

    readonly_fields = (
        'display_category',
        'dish',
        'display_subitems',
        'quantity',
    )

    fields = (
        'display_category',
        'dish',
        'display_subitems',
        'quantity',
    )

    def display_category(self, obj):
        return obj.dish.category.name
    display_category.short_description = "Category"

    def display_subitems(self, obj):
        if obj.subitems.exists():
            return ", ".join(sub.name for sub in obj.subitems.all())
        return "—"
    display_subitems.short_description = "Selected Sub-items"


# ===============================
# ORDER ADMIN
# ===============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'event_date',
        'delivery_address',
        'latitude',
        'longitude',
        'is_confirmed',
        'created_at',
    )

    list_filter = (
        'is_confirmed',
        'event_date',
    )

    search_fields = (
        'user__username',
    )

    inlines = [MenuSelectionInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user'
        ).prefetch_related(
            'selections__dish__category',
            'selections__subitems',
        )



# ===============================
# MENU STRUCTURE ADMIN
# ===============================

class DishInline(admin.TabularInline):
    model = Dish
    extra = 0


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price_info')
    list_filter = ('service_type',)
    inlines = [DishInline]


class SubItemInline(admin.TabularInline):
    model = SubItem
    extra = 0


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category__service_type',)
    inlines = [SubItemInline]


@admin.register(SubItem)
class SubItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish')
