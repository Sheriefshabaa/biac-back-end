from rest_framework import serializers
from .models import Classified_image
class ClassifiedImageSerializer (serializers.ModelSerializer):
    class Meta :
        model = Classified_image
        fields = '__all__'
    



