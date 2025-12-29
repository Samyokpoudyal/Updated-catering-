from django.urls import path
from django.contrib.auth import views as auth_views
from register.views import logout_view, profile
from .views import (
    AboutView, lunchbox_view, catering_view, 
    MenuItemsView, BookingServiceView, party_pack_menu_view,
    LunchboxMenuItemsView, PartyPackView, LunchboxPackView
)

urlpatterns = [
    path("", AboutView.as_view(), name='foodcateringweb.home'),
    
    # Function-based views for services
    path("partypack/", party_pack_menu_view, name='party'),
    path("partypackview/", PartyPackView.as_view(), name='partypackview'),
    path("lunchboxview/", LunchboxPackView.as_view(), name='lunchboxview'),
    path("lunchbox/", lunchbox_view, name='lunchbox'),
    path("catering/", catering_view, name='catering'),
    
    # Menu pages (ListView)
    path("menu/", MenuItemsView.as_view(), name='menuitemsview'),
    path("lmenu/", LunchboxMenuItemsView.as_view(), name='lunchboxmenuitemsview'),
    
    # Auth
    path("login/", auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path("logout/", logout_view, name='logout'),
    path("profile/", profile, name='profile'),
    
    # Password Reset
    path("passwordreset/", auth_views.PasswordResetView.as_view(template_name='register/password_reset.html'), name='change-password'),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'), name='password_reset_done'),
    path("password_reset_conform/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='register/password-reset-confirm.html'), name='password_reset_confirm'),
    
    # Booking and success pages
    path("booking/", BookingServiceView.as_view(), name='booking'),
    path("success/", BookingServiceView.as_view(), name='success'), 
]
