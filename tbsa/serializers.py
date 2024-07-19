from rest_framework import serializers

from users.models import CustomUser
from .models import Tbsa , Tbsa_image 



class ShowTbsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbsa
        fields = '__all__'

class TbsaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbsa_image
        fields = '__all__'



class TbsaBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbsa
        fields = ['id', 'patient_name', 'age_type', 'age', 'is_inhalation', 'weight']

    def create(self, validated_data):
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            validated_data['user_id'] = CustomUser.objects.get(email="guestbiacgp@gmail.com")
        else:
            validated_data['user_id'] = request_user
        
        tbsa = Tbsa.objects.create(**validated_data)
        return tbsa
    




class TbsaHandImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbsa_image
        fields = ['id','image']
    def create(self, validated_data):
        tbsa = Tbsa.objects.get(pk=self.context['tbsa_id'])
        return Tbsa_image.objects.create(image=validated_data['image'], image_type='H', tbsa_id=tbsa)
    


class TbsaBurnImagesSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )
    image_type ='B'

    def create(self, validated_data):
        tbsa_id = Tbsa.objects.get(pk=self.context['tbsa_id'])
        image_type = 'B'
        images = validated_data['images']
        
        tbsa_images = []
        for image in images:
            tbsa_image = Tbsa_image(tbsa_id=tbsa_id, image=image, image_type=image_type)
            tbsa_images.append(tbsa_image)
        
        Tbsa_image.objects.bulk_create(tbsa_images)
        return tbsa_images
    

