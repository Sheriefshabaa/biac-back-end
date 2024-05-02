# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from datetime import date, datetime
from users.models import GENDER_SELECTION, CustomUser

def calculateAge(date_of_birth):
    date_of_birth = date.fromisoformat(date_of_birth)
    today = date.today()
    years_difference = today.year - date_of_birth.year
    is_before_birthday = (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    age = years_difference - int(is_before_birthday)
    return age


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    phone_number = serializers.CharField(max_length=30)
    date_of_birth = serializers.DateField(required=False)
    profile_picture = serializers.ImageField(required=False)



    @transaction.atomic
    def save(self, request):
        """  """ 
        user = super().save(request)
        user.gender = self.data.get('gender')
        user.phone_number = self.data.get('phone_number')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.date_of_birth = self.data.get('date_of_birth')
        user.age = calculateAge(user.date_of_birth)
        user.user_image = self.validated_data.get('profile_picture', None)
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'date_of_birth',
            'is_premium',
            'is_active',
            'age',
            'user_image'
        )
        read_only_fields = ('pk', 'email', 'phone_number',)
