
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

class RegisterPermission(BasePermission):
    message='Sorry you have been denied from this activity'

    def has_object_permission(self, request, view, obj):
        user=User.objects.get(id=obj.user_id) 
        return user.username==request.user.username
        
        