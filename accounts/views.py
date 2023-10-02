from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import status


from .serializers import *
from .renderers import UserJSONRenderer


# Create your views here.



class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegisterationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        
        user = request.data.get('user', {})
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRUSerializer

    def retrieve(self, request, *args, **kwargs):

        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def update(self, request, *args, **kwargs):
        
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class RefreshTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RefreshTokenSerializer

    def post(self, request):

        user_data = request.data.get('user', {})
        
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AccessTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = AccessTokenSerializer

    def post(self, request):

        token = request.data.get('user', {})

        serializer = self.serializer_class(data=token)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class LogOutAPIView(APIView):
    # only if refresh token exists the user will be kept logged in
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        user = request.user
        token_deleter(user.id)
        msg = {'status':'logged out!'}

        return Response(msg, status=status.HTTP_200_OK)
    



class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {'status': 'Password changed succesfully.'}
        return Response(msg, status=status.HTTP_200_OK)