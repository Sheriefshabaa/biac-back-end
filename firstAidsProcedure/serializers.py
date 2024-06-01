from rest_framework import serializers

from .models import FirstAidsProcedure

class FirstAidsProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstAidsProcedure
        fields = '__all__'





