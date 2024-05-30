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
from image.serializers import imageFieldsSerializer
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


class ShowResultView(APIView):
    def get(self,request,id):
        classified_image = Classified_image.objects.get(id=id)
        classified_image_serializer = ClassifiedImageHistoryDataSerializer(classified_image)
        # print(classified_image_serializer)
        burn_degree = classified_image_serializer.data['burn_degree']
        first_aids_list = FirstAidsProcedure.objects.filter(procedure_for_degree=burn_degree).order_by('procedure_order')
        first_aids_serializer = FirstAidsProcedureSerializer(first_aids_list, many=True)
        result = {
            'classified_image': classified_image_serializer.data,
            'firstAidsList': first_aids_serializer,
        }
        return Response(result, status=status.HTTP_200_OK)
    

class DownloadResultsAsPDFView(APIView):
    def get(self,request,id):
        try:
            classified_image = Classified_image.objects.get(id=id)
            classified_image_serializer = ClassifiedImageSerializer(classified_image)
            image = Image.objects.get(id=classified_image_serializer.data['image_id'])
            image_serializer = imageFieldsSerializer(image)
            first_aids = FirstAidsProcedure.objects.filter(procedure_for_degree=classified_image_serializer.data['burn_degree']).order_by('procedure_order')
            first_aids_serializer = FirstAidsProcedureSerializer(first_aids, many=True)
            buffer = BytesIO()

            # Create the PDF object, using the buffer as its "file"
            p = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            image1_path = os.path.join(settings.MEDIA_ROOT, image.provided_image.name)
            image2_path = os.path.join(settings.MEDIA_ROOT, classified_image.image_with_model_classification.name)

            p.drawImage(image1_path, 100, 600, width=200, height=150)
            p.drawImage(image2_path, 100, 400, width=200, height=150)  # Adjust position to avoid overlap
            y_position = 350
            for first_aid in first_aids_serializer.data:
                p.drawString(100, y_position, first_aid['procedure'])
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



