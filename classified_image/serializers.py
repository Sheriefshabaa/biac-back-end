from rest_framework import serializers
from .models import Classified_image
class ClassifiedImageSerializer (serializers.ModelSerializer):
    class Meta :
        model = Classified_image
        fields = '__all__'
    

class ClassifiedImageHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classified_image
        fields = ['id','image_with_model_classification', 'confidence_score', 'burn_degree']
