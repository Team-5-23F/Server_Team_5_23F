from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class WritingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        writing_id = request.GET.get('writing_id', None)
        if writing_id is None:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        
        writing = get_object_or_404(Writing, pk=writing_id)

        serializer = WritingSerializer(data=writing)
        if not serializer.is_valid():
            print(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        writing_data = {
            "format":request.data['format'],
            "purpose":request.data['purpose']
        }
        serializer = WritingCreateSerializer(data=writing_data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save(writer=request.user)

        writing = get_object_or_404(Writing, pk=serializer.data["id"])
        paragraph_data_list = request.data['paragraphs']
        for paragraph_data in paragraph_data_list:
            print(paragraph_data)
            serializer_para = ParagraphCreateSerializer(data = paragraph_data)
            if serializer_para.is_valid():
                serializer_para.save(writing=writing)
        
        return_serializer = WritingSerializer(data=writing)
        if not return_serializer.is_valid():
           return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        return Response(return_serializer.data,status=status.HTTP_200_OK)

class WritingListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        writings = Writing.objects.filter(writer=request.user)
        if not writings.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        serializer = WritingListModelSerializer(data=writings, many=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ParagraphListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paragraphs = Paragraph.objects.filter(writer=request.user,bookmark=True)
        serializer = ParagraphSerializer(data=paragraphs,many=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
