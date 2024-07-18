# serializers.py in the users Django app
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from datetime import date
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser 
from image.models import Image 
from classified_image.serializers import ClassifiedImageHistoryDataSerializer
from allauth.account.utils import send_email_confirmation
from datetime import datetime




class CustomRegisterSerializer(RegisterSerializer):
    """ this function takes the user data for registration
    and if the data are valid it creates a user object in database  
    """
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
  
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
  
    @transaction.atomic
    def save(self, request):
        """  
        this function is taking the input from user 
        -> validate the input 
        -> create a object in database 
        -> returned the new user object
        """ 
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.is_active = False
        user.is_active = False
        user.save()
        send_email_confirmation(request, user)
        send_email_confirmation(request, user)
        return user




def calculateAge(date_of_birth):
    date_of_birth = date.fromisoformat(date_of_birth)
    today = date.today()
    years_difference = today.year - date_of_birth.year
    is_before_birthday = (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
    age = years_difference - int(is_before_birthday)
    return age




class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender','phone_number', 'date_of_birth', 'user_image']


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        instance.save()
        return instance





class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender','phone_number', 'date_of_birth', 'user_image']


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        instance.save()
        return instance



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
            'user_id': user_serializer.data['pk'],
            'user_id': user_serializer.data['pk'],
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






def reformat_date(date):
    datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_str = datetime_obj.strftime("%Y-%m-%d")
    return date_str

class HistoryUserClassifiedImagesSerializer(serializers.ModelSerializer):
    classified_images = ClassifiedImageHistoryDataSerializer(many=True, read_only=True)
    provided_image = serializers.ImageField()
    captured_at = serializers.DateTimeField()

    class Meta:
        model = Image
        fields = ['id', 'provided_image', 'captured_at', 'classified_images']

    def to_representation(self, instance):
        """
        Convert the instance to a representation that includes both
        fields from the Image model and classified images.
        """
        request = self.context.get('request')
        data = super().to_representation(instance)


        # reformate the date representation
        data['captured_at'] = reformat_date(data['captured_at'])

        # Build absolute URI for provided_image
        if request:
            provided_image_url = instance.provided_image.url
            data['provided_image'] = request.build_absolute_uri(provided_image_url)

        # Serialize classified images and build absolute URI for image_with_model_classification
        classified_images = instance.classified_image.all()
        classified_images_data = ClassifiedImageHistoryDataSerializer(classified_images, many=True, context={'request': request}).data
        
        for classified_image in classified_images_data:
            if request:
                image_with_model_classification_url = classified_image['image_with_model_classification']
                classified_image['image_with_model_classification'] = request.build_absolute_uri(image_with_model_classification_url)
        
        data['classified_images'] = classified_images_data

        return data
