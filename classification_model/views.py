# views.py

import uuid
from rest_framework.response import Response
from rest_framework.views import APIView
import torch
from .serializers import imgSerializer
from rest_framework.parsers import (MultiPartParser, FormParser)
from django.conf import settings

from ultralytics import YOLO
from PIL import Image


from .models import ClassificationBurn

# Load the pre-trained PyTorch model





class ImageProcessingView(APIView):
    queryset = ClassificationBurn.objects.order_by('id')
    serializer_class = imgSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request,format=None):
        input_serializer = imgSerializer(data=request.data)
        if input_serializer.is_valid():
            instance = input_serializer.save()
            image_file = request.FILES.get('img_url_before')
            if not image_file:
                return Response({'error': 'No image uploaded'}, status=400)
            # print(image_file.name)
            image_path = f"media/input_images/{image_file.name}"
            input_image = Image.open(image_path)
            image_resized = input_image.resize([300, 300])  # Resize (adjust as needed)
            # Load YOLO model
            model_file_path = 'model/best.pt'
            model = YOLO(model_file_path)
            # Make prediction
            prediction = model.predict(image_resized,conf=0.5)
 
            box_corr=prediction[0].boxes.xywh
            box_conf=prediction[0].boxes.conf
            print(box_corr)
            print(box_conf)
            # prediction = model.predict(image_resized)
            my_uuid = uuid.uuid4()
            output_image_path = f"media/output_images/prediction_{image_file.name}_{my_uuid}.jpg"
            # print(prediction[0])
            # Save the prediction output image
            prediction[0].save(output_image_path)
            # Update the same instance with the output image path
            instance.img_url_after = output_image_path
            instance.save()
            return Response("alhamdulillah", status=200)
        else:
            return Response(data=input_serializer.errors, status=400)
