from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginTokenObtainPairSerializer
from rest_framework.parsers import (MultiPartParser, FormParser)
from rest_framework import status

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginTokenObtainPairSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = LoginTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response(serializer.validated_data)






class LogoutBlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

