from io import BytesIO
from django.shortcuts import render

import requests
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from classified_image.models import Classified_image
from classified_image.serializers import ClassifiedImageHistoryDataSerializer, ClassifiedImageSerializer
from image.models import Image
from image.serializers import ImageFieldsSerializer ,GetImageSerializer
from .models import FirstAidsProcedure
from rest_framework import status
from .serializers import FirstAidsProcedureSerializer
# Create your views here.

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ShowResultView(APIView):
    def get(self, request, id):
        classified_image = Classified_image.objects.get(id=id)
        classified_image_serializer = ClassifiedImageHistoryDataSerializer(classified_image, context={'request': request})

        # image = Image.objects.get(id=classified_image.image_id)

        provided_image_serializer = GetImageSerializer(classified_image.image_id)


        
        burn_degree = classified_image_serializer.data['burn_degree']
        first_aids_list = FirstAidsProcedure.objects.filter(procedure_for_degree=burn_degree).order_by('procedure_order')
        first_aids_serializer = FirstAidsProcedureSerializer(first_aids_list, many=True)
        
        result = {
            'classified_image': classified_image_serializer.data,
            'firstAidsList': first_aids_serializer.data,
            'provided_image':provided_image_serializer.data,
        }
        return Response(result, status=status.HTTP_200_OK)

class DownloadResultsAsPDFView(APIView):
    def get(self, request, id):
        try:
            classified_image = Classified_image.objects.get(id=id)
            classified_image_serializer = ClassifiedImageSerializer(classified_image)
            image = Image.objects.get(id=classified_image_serializer.data['image_id'])
            first_aids = FirstAidsProcedure.objects.filter(procedure_for_degree=classified_image_serializer.data['burn_degree']).order_by('procedure_order')
            first_aids_serializer = FirstAidsProcedureSerializer(first_aids, many=True)
            buffer = BytesIO()

            # Create the PDF object, using the buffer as its "file"
            p = canvas.Canvas(buffer, pagesize=A4)

            # Starting positions
            x_position = 100
            y_position = 800
            image_width = 200
            image_height = 150
            text_offset = 20  # Space between text and images
            image_gap = 20    # Space between images

            # Draw text and images
            p.drawString(x_position, y_position, "Image before classification:")
            image1_path = os.path.join(settings.MEDIA_ROOT, image.provided_image.name)
            p.drawImage(image1_path, x_position, y_position - image_height - text_offset, width=image_width, height=image_height)

            p.drawString(x_position + image_width + image_gap, y_position, "Image after classification:")
            image2_path = os.path.join(settings.MEDIA_ROOT, classified_image.image_with_model_classification.name)
            p.drawImage(image2_path, x_position + image_width + image_gap, y_position - image_height - text_offset, width=image_width, height=image_height)

            # Draw the first aid procedures
            y_position -= (image_height + text_offset + 20)  # Adjust position below the images
            p.drawString(x_position, y_position, "First Aids procedure:")
            y_position -= text_offset

            for first_aid in first_aids_serializer.data:
                p.drawString(x_position, y_position, f"{first_aid['procedure_order']}- {first_aid['procedure']}")
                y_position -= 20  # Move to next line

            p.showPage()
            p.save()

            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
            response.write(pdf)
            return response
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)