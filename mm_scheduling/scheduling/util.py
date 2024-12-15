# from rest_framework.authentication import BaseAuthentication
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
# from django.contrib.auth.models import AnonymousUser
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.authentication import JWTAuthentication
# import jwt
# from django.conf import settings
import logging

logger = logging.getLogger('scheduling')


def get_correlation_id(request):
    return getattr(request, 'correlation_id', 'N/A')

class RemoteJWTAuthenticationDeprecated(JWTAuthentication):
    def authenticate(self, request):
        correlation_id = get_correlation_id(request)
        logger.info(f'Authenticating user with depricated method', extra={'correlation_id': correlation_id})

        raw_token = self.get_raw_token(self.get_header(request))
        if raw_token is None:
            logger.warning('No raw token found', extra={'correlation_id': correlation_id})
            return None

        validated_token = self.get_validated_token(raw_token)
        # Trust the `user_id` in the token instead of querying a local database
        user_id = validated_token.get("user_id")
        if not user_id:
            logger.error('Invalid token: no user_id', extra={'correlation_id': correlation_id})
            raise AuthenticationFailed("Invalid token: no user_id")

        # Optionally attach `user_id` to the request for further use
        request.user = {"id": user_id, "is_authenticated": True}
        logger.info(f'User authenticated: {user_id}', extra={'correlation_id': correlation_id})
        return (request.user, validated_token)


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow anyone to retrieve an object (GET),
    but restrict Update and Delete actions to the owner.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            print("Using GET, allowing request")
            return True
        # Write permissions are only allowed to the owner
        print(f"obj.organizer_id: {obj.organizer_id}")
        print(f"request.user.id: {request.user.id}")
        return obj.organizer_id == request.user.id


class RemoteJWTAuthentication(JWTAuthentication):
    AUTH_SERVICE_URL = "http://localhost:8001/userinfo/" #################################################

    def get_header(self, request):
        header = request.headers.get("Authorization")
        if isinstance(header, bytes):
            header = header.decode("utf-8")
        return header

    def authenticate(self, request):
        self.correlation_id = get_correlation_id(request)
        logger.info('Authenticating user via remote service', extra={'correlation_id': self.correlation_id})

        validated_token = self.get_validated_token(self.get_raw_token(request))
        user_info = self.fetch_user_info(validated_token)

        if not user_info:
            logger.error('User not found during authentication', extra={'correlation_id': self.correlation_id})
            raise AuthenticationFailed("User not found")

        request.user = self.create_user_representation(user_info)
        logger.info(f'User authenticated: {request.user}', extra={'correlation_id': self.correlation_id})
        return (request.user, validated_token)

    def fetch_user_info(self, token):
        headers = {"Authorization": f"Bearer {token}",
                   "X-Correlation-ID": self.correlation_id}
        logger.debug(f'Fetching user info from {self.AUTH_SERVICE_URL}', extra={'correlation_id': self.correlation_id})

        try:
            response = requests.get(self.AUTH_SERVICE_URL, headers=headers)
            logger.info(f'Auth service response status: {response.status_code}', extra={'correlation_id': self.correlation_id})
            if response.status_code == 200:
                logger.debug('User info retrieved successfully', extra={'correlation_id': self.correlation_id})
                return response.json()
        except requests.RequestException as e:
            logger.error(f'Error fetching user info: {e}', extra={'correlation_id': self.correlation_id})
        return None

    def create_user_representation(self, user_info):
        # Create a simple user-like object
        logger.debug(f'Creating user representation for {user_info}', extra={'correlation_id': self.correlation_id})
        class RemoteUser:
            def __init__(self, info):
                self.id = info.get("id")
                self.username = info.get("username")
                self.email = info.get("email")
                self.is_authenticated = True  # Django requires this

            def __str__(self):
                return self.username or "Anonymous"

        return RemoteUser(user_info)

    def get_raw_token(self, request):
        header = self.get_header(request)
        if not header:
            logger.warning('Authorization header missing', extra={'correlation_id': self.correlation_id})
            raise AuthenticationFailed("Authorization header missing")

        logger.debug('Authorization Header found', extra={'correlation_id': self.correlation_id})

        # Extract token
        parts = header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.error("Authorization header must be 'Bearer <token>'", extra={'correlation_id': self.correlation_id})
            raise AuthenticationFailed(
                "Authorization header must be 'Bearer <token>'")

        return parts[1]
