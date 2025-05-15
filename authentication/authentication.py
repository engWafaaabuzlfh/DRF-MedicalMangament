# src/authentication/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ActiveAccessToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        
        user, validated_token = result
        raw_token = request.headers.get("Authorization", "").split(" ")[1]
        if not ActiveAccessToken.objects.filter(token=raw_token).exists():
            raise AuthenticationFailed({
                "detail": "Given token is not valid for any token type",
                "code": "token_not_valid",
                "messages": [
                    {
                        "token_class": "AccessToken",
                        "token_type": "access",
                        "message": "Token is invalid or expired"
                    }
                ]
            })
        return user, validated_token

