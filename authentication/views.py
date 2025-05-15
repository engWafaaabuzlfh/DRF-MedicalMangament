from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, ActiveAccessToken
from datetime import datetime, timedelta

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token_str = request.data.get("refresh")

        try:
            refresh_token = RefreshToken(refresh_token_str, verify=False)
            
            refresh_token.check_blacklist()
        
        except TokenError as e:
            return Response({
                "detail": "Token is invalid or expired",
                "code": "token_blacklisted",
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, *args, **kwargs)

        access_token = response.data.get("access")
        user_id = refresh_token.get("user_id")
        user = User.objects.get(id=user_id)

        if access_token:
            ActiveAccessToken.objects.create(
                token=access_token,
                user=user
            )

        return response
#Custom jwt Authentication


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            ActiveAccessToken.objects.create(user=user, token=access_token).save()
            return Response({"message": "Login Successfully",
            'refresh_token' : str(refresh),
            'access_token': access_token
            ,'user':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        ActiveAccessToken.objects.create(user=user, token=access_token).save()
        
        return Response({
            "message": "Login Successfully",
            'refresh_token' : str(refresh),
            'access_token': access_token,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            access_token = request.headers.get("Authorization", "").split(" ")[1]
            user = request.user
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # إضافة التوكن لقائمة الحظر
                ActiveAccessToken.objects.filter(token=access_token).delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

