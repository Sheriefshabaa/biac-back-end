from django.contrib.auth.models import Group, User
from rest_framework import serializers
from PIL import Image as pil_image
from image.models import Image
from .models import CustomUser



class ImageFieldsSerializer (serializers.ModelSerializer):    
    class Meta :
        model = Image
        fields = '__all__'

class GetImageSerializer(serializers.ModelSerializer):
    class Meta :
       model = Image
       fields = ['provided_image']




class ImageSerializer (serializers.ModelSerializer):
    provided_image = serializers.ImageField(required=True)

    class Meta :
        model = Image
        fields = ['provided_image']

    def create(self, validated_data):
        request_user = self.context['request'].user
        request_user = self.context['request'].user
        provided_image = self.validated_data.get('provided_image', None)
        image = pil_image.open(provided_image)
        image_width, image_height = image.size
        if request_user.is_anonymous:
            validated_data['user'] = CustomUser.objects.get(email="guestbiacgp@gmail.com")
        else:
            validated_data['user'] = request_user
        return Image.objects.create(
            **validated_data,
            image_width=image_width,
            image_height=image_height,
        )
    

    
