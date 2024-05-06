# serializers.py in the users Django app
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer
from datetime import date
from .models import GENDER_SELECTION
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    """ this function takes the user data for registration
    and if the data are valid it creates a user object in database  
    """
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    gender = serializers.ChoiceField(choices=GENDER_SELECTION, required=False)
    phone_number = serializers.CharField(max_length=30, required=False)
    date_of_birth = serializers.DateField(required=False)
    profile_picture = serializers.ImageField(required=False)

    @transaction.atomic
    def save(self, request):
        """  
        this function is taking the input from user 
        -> validate the input 
        -> create a object in database 
        -> returned the new user object
        """
        user = super().save(request)
        user.gender = self.data.get('gender')
        user.phone_number = self.data.get('phone_number')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.date_of_birth = self.data.get('date_of_birth')
        if user.date_of_birth:
            user.age = calculateAge(user.date_of_birth)
        user.user_image = self.validated_data.get('profile_picture', None)
        user.save()
        return user


def calculateAge(date_of_birth):
    date_of_birth = date.fromisoformat(date_of_birth)
    today = date.today()
    years_difference = today.year - date_of_birth.year
    is_before_birthday = (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    age = years_difference - int(is_before_birthday)
    return age


class LoginTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')

        # Authentication logic
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        # Return tokens and user data (using custom user serializer)
        token = RefreshToken.for_user(user)
        user_serializer = CustomUserDetailsSerializer(user)
        return {
            'token': str(token.access_token),
            'refresh': str(token),  # Include refresh token if needed
            'user': user_serializer.data
        }


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
