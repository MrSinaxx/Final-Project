import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import APIException
from .models import CustomUser
from .utils import *


class TokenException(APIException):
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = '403'


class JWTAuthentication(authentication.BaseAuthentication):
    """JWT based authentication for the REST framework. This class isn't provided by DRF."""
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        '''
        Check the header for token. and return (user, token).
        '''
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None
        
        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None
        

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")
        

        if prefix.lower() != auth_header_prefix:
            return None
        

        token_type = check_token_type(token)

     
        if token_type != "access":
            raise TokenException('Invalid Token!')
        return self._authenticate_credentials(request, token)

    

    def _authenticate_credentials(self, request, token):
        '''
        Check token credentials. and catch exceptions. then return (user, token).
        '''
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = "Invalid authentication. Could not decode token."
            raise TokenException(msg)
        
        try:
            user = CustomUser.objects.get(pk=payload["user_id"])
        except CustomUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = "This user has been deactivated"
            raise AuthenticationFailed(msg)
        
        return(user, token)