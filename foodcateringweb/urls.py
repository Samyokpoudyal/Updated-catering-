"""foodcatering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import AboutView, LunchboxView,PartyPackView,CateringServiceView,MenuItemsView,BookingServiceView,party_pack_menu_view
from django.contrib.auth import views as auth_views
from register.views import logout_view, profile
from . import views

urlpatterns = [
    path("", AboutView.as_view(),name='foodcateringweb.home'),
    path("partypack/", PartyPackView.as_view(),name='party'),
    path("lunchbox/", LunchboxView.as_view(),name='lunchbox'),
    path("catering/", CateringServiceView.as_view(),name='catering'),
    path("menu/", MenuItemsView.as_view(),name='menuitemsview'),
    path("login/",auth_views.LoginView.as_view(template_name='register/login.html'),name='login'),
    path("logout/",logout_view,name='logout'),
    path("profile/",profile,name='profile'),
    path("passwordreset/",auth_views.PasswordResetView.as_view(template_name='register/password_reset.html'),name='change-password'),
    path("password_reset_done/",auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'),name='password_reset_done'),
    path("password_reset_conform/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='register/password-reset-confirm.html'),name='password_reset_confirm'),
    path("booking/", BookingServiceView.as_view(),name='booking'),
    path('success',party_pack_menu_view,name='success')
]