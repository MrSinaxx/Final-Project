from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from .authentication import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)
from .serializers import UserSerializer
from .models import User


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data["email"]).first()

        if not user:
            raise APIException("Invalid credentials!")

        if not user.check_password(request.data["password"]):
            raise APIException("Invalid credentials!")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key="refreshToken", value=refresh_token, httponly=True)
        response.data = {"token": access_token}

        return response
