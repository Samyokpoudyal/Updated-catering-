from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ('user', 'status', 'event_date', 'delivery_address', 'created_at')
    list_filter = ('status', 'event_date', 'created_at')
    list_editable = ('status',)  # admin can edit this column directly
    search_fields = ('user__username', 'delivery_address')
    inlines = [MenuSelectionInline]


    def colored_status(self, obj):
        colors = {
            'processing': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
        }
        return format_html('<b style="color:{}">{}</b>', colors.get(obj.status, 'black'), obj.get_status_display())
    colored_status.short_description = "Order Status"



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
