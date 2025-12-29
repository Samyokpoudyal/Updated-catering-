from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import MenuCategory, Dish, SubItem, MenuSelection, Order, User

# --- STATIC PAGES ---
class AboutView(TemplateView):
    template_name = "foodcateringtem/frontend.html"

class PartyPackView(TemplateView):
    template_name = "foodcateringtem/partypack.html"

class LunchboxPackView(TemplateView):
    template_name = "foodcateringtem/lunchbox.html"

# --- LIST VIEWS FOR MENUS ---
class MenuItemsView(ListView):
    model = MenuCategory
    template_name = "foodcateringtem/menu.html"
    context_object_name = "categories"

    def get_queryset(self):
        return MenuCategory.objects.order_by('service_type').prefetch_related('dishes__subitems')

class LunchboxMenuItemsView(ListView):
    model = MenuCategory
    template_name = "foodcateringtem/lunchboxmenu.html"
    context_object_name = "categories"

    def get_queryset(self):
        return MenuCategory.objects.order_by('service_type').prefetch_related('dishes__subitems')

class BookingServiceView(TemplateView):
    template_name = "foodcateringtem/conform.html"

# --- REUSABLE ORDER PROCESSING LOGIC ---
def process_menu_order(request, category_id, event_date):
    category = get_object_or_404(MenuCategory, id=category_id)
    
    # --- GET LOCATION DATA ---
    delivery_address = request.POST.get('delivery_address', '')
    latitude = request.POST.get('latitude') or None
    longitude = request.POST.get('longitude') or None

    order = Order.objects.create(
        user=request.user,
        event_date=event_date,
        delivery_address=delivery_address,
        latitude=latitude,
        longitude=longitude
    )

    # --- Dishes without subitems ---
    selected_dish_ids = request.POST.getlist(f'dishes_{category.id}')
    for dish_id in selected_dish_ids:
        dish = Dish.objects.get(id=dish_id, category=category)
        MenuSelection.objects.create(order=order, dish=dish)

    # --- Dishes with subitems ---
    for dish in category.dishes.all():
        subitem_ids = request.POST.getlist(f'dish_{dish.id}')
        if subitem_ids:
            selection = MenuSelection.objects.create(order=order, dish=dish)
            selection.subitems.set(SubItem.objects.filter(id__in=subitem_ids))
    
    return order, category  # return category for email

# --- EMAIL FUNCTION ---
def send_order_confirmation_email(user, order, category):
    message = render_to_string('foodcateringtem/email.html', {
        'user': user,
        'order': order,
        'category': category,
    })
    email = EmailMessage(
        subject="Your Order is Confirmed!",
        body=message,
        from_email='poudyalsamyok@gmail.com',  # or settings.EMAIL_HOST_USER
        to=[user.email],
    )
    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        print("Email sending failed:", e)

# --- MENU VIEWS WITH EMAIL NOTIFICATION ---

def party_pack_menu_view(request):
    categories = MenuCategory.objects.filter(service_type='party_pack').prefetch_related('dishes__subitems')
    
    if request.method == 'POST':
        order, category = process_menu_order(
            request,
            request.POST.get('category_id'),
            request.POST.get('event_date')
        )
        send_order_confirmation_email(request.user, order, category)
        return redirect('success')

    return render(request, 'foodcateringtem/service_menu.html', {
        'categories': categories,
        'service_type': 'party_pack'
    })
    

def lunchbox_view(request):
    categories = MenuCategory.objects.filter(service_type='lunchbox').prefetch_related('dishes__subitems')
    
    if request.method == 'POST':
        order, category = process_menu_order(
            request,
            request.POST.get('category_id'),
            request.POST.get('event_date')
        )
        send_order_confirmation_email(request.user, order, category)
        return redirect('success')

    return render(request, 'foodcateringtem/service_menu.html', {
        'categories': categories,
        'service_type': 'lunchbox'
    })

@login_required
def catering_view(request):
    categories = MenuCategory.objects.filter(service_type='catering').prefetch_related('dishes__subitems')
    
    if request.method == 'POST':
        order, category = process_menu_order(
            request,
            request.POST.get('category_id'),
            request.POST.get('event_date')
        )
        send_order_confirmation_email(request.user, order, category)
        return redirect('success')

    return render(request, 'foodcateringtem/service_menu.html', {
        'categories': categories,
        'service_type': 'catering'
    })
