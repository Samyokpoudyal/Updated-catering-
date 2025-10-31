from django.urls import path
from .views import *


urlpatterns = [
    
    path('',ProfileSerializerListView.as_view(),name='register-api'),
    path('detail/<int:id>/',ProfileSerializerDetailView.as_view(),name='register-detail'),
    path('create/',CreateProfileView.as_view(),name='register-create')
]

