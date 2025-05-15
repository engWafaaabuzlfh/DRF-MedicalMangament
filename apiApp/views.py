from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from .serializers import PatiantSerializer
from .models import Patiant, Invoice, Diagnosis
from rest_framework.permissions import IsAuthenticated


class PatiantView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        patients = Patiant.objects.filter(doctor=user)
        serializer = PatiantSerializer(patients, many=True)
        return Response({'patients':serializer.data})
    
    def post(self, request):
        user = request.user
        print('user', user)
        serializer = PatiantSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(doctor=user)
            return Response({"message": "patient created successfully",
                             'data': serializer.data}, status=status.HTTP_200_OK)
        
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePatiantView(RetrieveUpdateAPIView):
    queryset = Patiant.objects.all()
    serializer_class = PatiantSerializer
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        patient = self.get_object()
        print('pp',patient)
        if patient.doctor != user:
            return Response({'error': 'Not allowed'}, status=403)
        
        return self.partial_update(request, *args, **kwargs)
        
        