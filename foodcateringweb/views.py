from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView
from .models import MenuCategory, Dish, DishOption,MenuSelection,Order




class AboutView(TemplateView):
    template_name = "foodcateringtem/frontend.html"


class LunchboxView(TemplateView):
    template_name = "foodcateringtem/lunchbox.html"


class PartyPackView(TemplateView):
    template_name = "foodcateringtem/partypack.html"


class CateringServiceView(TemplateView):
    template_name = "foodcateringtem/catering.html"


class MenuItemsView(ListView):
    model = MenuCategory
    template_name = "foodcateringtem/menu.html"
    context_object_name = "categories"

    def get_queryset(self):
        return MenuCategory.objects.prefetch_related('dishes').all()


# You had two BookingServiceView classes — keeping just one:
class BookingServiceView(TemplateView):
    template_name = "foodcateringtem/conform.html"


@login_required
def party_pack_menu_view(request):
    categories = MenuCategory.objects.prefetch_related('dishes__options1').all()

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        event_date = request.POST.get('event_date')

        # Get the category
        category = MenuCategory.objects.get(id=category_id)

        # Create or get an order for this user + event date
        order, created = Order.objects.get_or_create(
            user=request.user,
            event_date=event_date
        )

        # Save checked dishes without options
        selected_dishes = request.POST.getlist(f'dishes_{category.id}')
        for dish_id in selected_dishes:
            dish = Dish.objects.get(id=dish_id, category=category)
            # Check if selection already exists
            selection, sel_created = MenuSelection.objects.get_or_create(
                order=order,
                dish=dish,
                option=None
            )
            if not sel_created:
                # Optional: increment quantity if already exists
                selection.quantity += 1
                selection.save()

        # Save dishes with selected options
        for dish_with_options in category.dishes.filter(options1__isnull=False):
            option_id = request.POST.get(f'dish_{dish_with_options.id}')
            if option_id:
                option = DishOption.objects.get(id=option_id, dish_subtype=dish_with_options)
                selection, sel_created = MenuSelection.objects.get_or_create(
                    order=order,
                    dish=dish_with_options,
                    option=option
                )
                if not sel_created:
                    # Optional: increment quantity if already exists
                    selection.quantity += 1
                    selection.save()

        # Redirect to success page
        return redirect('success')

    return render(request, 'foodcateringtem/success.html', {'categories': categories})

