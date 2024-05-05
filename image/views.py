import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from .serializers import imageSerializer
from rest_framework.parsers import (MultiPartParser, FormParser)
from rest_framework import status


class UploadImageView(APIView):
    serializer_class = imageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = imageSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            image = serializer.save()
            image_id = image.id
            response = requests.post(f'http://127.0.0.1:8000//classification/classified_image/{image_id}/')
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
