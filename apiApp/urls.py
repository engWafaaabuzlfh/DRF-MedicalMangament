from django.urls import path
from .views import PatiantView, UpdatePatiantView
urlpatterns = [
    path('my-patients/', PatiantView.as_view(), name='MYPatients'),
    path('my-patients/<int:pk>/', UpdatePatiantView.as_view(), name='MYPatientsUpdate'),
]