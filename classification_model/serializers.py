from django.contrib.auth.models import Group, User
from rest_framework import serializers

from classification_model.models import ClassificationBurn



class imgSerializer (serializers.ModelSerializer):
    class Meta :
        model = ClassificationBurn
        fields = ['img_url_before']


    def create(self, validated_data):
        img_url_before = validated_data.get('img_url_before')
        cBurn = ClassificationBurn.objects.create(img_url_before=img_url_before)
        return cBurn