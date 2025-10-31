from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField,ValidationError
from ..models import Profiles
from django.contrib.auth.models import User
from rest_framework.response import Response 

class ProfileSerializers(ModelSerializer):
    profile_name=SerializerMethodField()
    details=HyperlinkedIdentityField(
        view_name='register-detail',
        lookup_field ='id'
    )
    class Meta:
        model=Profiles
        fields=['id','profile_name','user','details']

    def get_profile_name(self,obj):
        return obj.user.username

class ProfileDetailSerializers(ModelSerializer):
    blogs=SerializerMethodField()

    class Meta:
        model=Profiles
        fields='__all__'
        
    def get_blogs(self,obj):
        datas=obj.user.articles_set.all()
        return datas.values()
    

class ProfileCreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']

    def validate(self, attrs):
        if (attrs['first_name']==""or attrs['last_name']==""):
            raise ValidationError('Please Fill all the informations on the field')
        
        else:
           return attrs
       
    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'],
                                 first_name=validated_data['first_name'],
                                 last_name=validated_data['last_name'],
                                 password=validated_data['password'],
                                 email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user




















