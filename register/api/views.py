from .serializers import *
from rest_framework.generics import *
from blog.api.pagination import MyCustomPageNumberPagination
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .permissions import RegisterPermission
from ..models import Profiles
from django.contrib.auth.models import User

class ProfileSerializerListView(ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Profiles.objects.all()
    serializer_class=ProfileSerializers
    pagination_class=MyCustomPageNumberPagination
    filter_backends=[filters.SearchFilter,filters.OrderingFilter]


class ProfileSerializerDetailView(RetrieveAPIView):
    permission_classes=[IsAuthenticated,RegisterPermission]
    queryset=Profiles.objects.all()
    serializer_class=ProfileDetailSerializers
    lookup_field='id'


class CreateProfileView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ProfileCreationSerializer


    