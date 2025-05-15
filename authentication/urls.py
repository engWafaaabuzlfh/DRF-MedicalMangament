from django.urls import path
from .views import RegisterView, LoginView, CustomTokenRefreshView, UserProfileUpdateView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='RegisterForm'),
    path('login/', LoginView.as_view(), name='LoginForm'),
    path('token/', CustomTokenRefreshView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileUpdateView.as_view(), name='UpdateUser'),
    path('logout/', LogoutView.as_view(), name='Logout'),

]