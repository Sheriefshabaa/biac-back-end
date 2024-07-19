from rest_framework import serializers
from .models import Classified_image
class ClassifiedImageSerializer (serializers.ModelSerializer):
    class Meta :
        model = Classified_image
        fields = '__all__'

    # def get_photo_url(self , obj):
    #     request = self.context.get('request')
    #     image_url = obj.fingerprint.url
    #     return request.build_absolute_url(image_url)
    

class ClassifiedImageHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classified_image
        fields = ['id', 'image_with_model_classification', 'confidence_score', 'burn_degree']

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        
        # Build absolute URI for image_with_model_classification
        if request:
            image_with_model_classification_url = instance.image_with_model_classification.url
            data['image_with_model_classification'] = request.build_absolute_uri(image_with_model_classification_url)
        
        return data
