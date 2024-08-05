from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import LoginObtainPairSerializer , HistoryUserClassifiedImagesSerializer , UpdateProfileSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import CustomUser
from rest_framework import status
from image.models import Image
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginObtainPairSerializer
    # parser_classes = [JSONParser]
    # parser_classes = [JSONParser]
    def post(self, request, format=None):
        serializer = LoginObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response(serializer.validated_data)



class UpdateProfileView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
class UpdateProfileView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=self.kwargs['id'])
        except CustomUser.DoesNotExist:
            return Response('the user does not exist', status=status.HTTP_401_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=self.kwargs['id'])
        except CustomUser.DoesNotExist:
            return Response('the user does not exist', status=status.HTTP_401_BAD_REQUEST)

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        




# returns the name of degree burn and the time that classification happend in and the image of classified image
class HistoryUserView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, id , *args,**kwargs):
        images = Image.objects.filter(user_id=id)
        serialized_data = HistoryUserClassifiedImagesSerializer(images, many=True, context={'request': request}).data
        return Response(serialized_data, status=status.HTTP_200_OK)


