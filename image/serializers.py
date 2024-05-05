from django.contrib.auth.models import Group, User
from rest_framework import serializers
from PIL import Image as pil_image
from image.models import Image



class imageSerializer (serializers.ModelSerializer):
    provided_image = serializers.ImageField(required=True)
    class Meta :
        model = Image
        fields = ['provided_image']


    def create(self, validated_data):
        provided_image = self.validated_data.get('provided_image', None)
        image = pil_image.open(provided_image)
        image_width, image_height = image.size
        validated_data['user'] = self.context['request'].user
        return Image.objects.create(
            **validated_data,
            image_width=image_width,
            image_height=image_height,
        )
        