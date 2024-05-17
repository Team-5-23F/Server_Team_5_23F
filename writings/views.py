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
        user = request.user
        writing_id = request.GET.get('writing_id', None)
        if writing_id is None:
            # 리스트
            writings = Writing.objects.filter(writer=request.user)
            if not writings.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            serializer = WritingListModelSerializer(writings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        writing = get_object_or_404(Writing,pk=writing_id, writer=user)
        serializer = WritingSerializer(writing)
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

        writing = get_object_or_404(Writing, pk=serializer.data["pk"])
        paragraph_data_list = request.data['paragraphs']
        for paragraph_data in paragraph_data_list:
            #print(paragraph_data)
            serializer_para = ParagraphCreateSerializer(data = paragraph_data)
            if serializer_para.is_valid():
                serializer_para.save(writing=writing)
        
        return Response(WritingSerializer(writing).data,status=status.HTTP_200_OK)
    def delete(self, request):
        delete_blog = Writing.objects.get(pk=request.GET.get('writing_id', None),writer=request.user)
        delete_blog.delete()

        return Response(status=status.HTTP_202_ACCEPTED)


class ParagraphListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paragraph_id = request.GET.get('paragraph_id', None)
        if paragraph_id is None:
            writings = Writing.objects.filter(writer=request.user)
            paragraphs = Paragraph.objects.filter(writing__in=writings,bookmark=True)
            serializer = ParagraphListModelSerializer(paragraphs,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            writings = Writing.objects.filter(writer=request.user)
            paragraph = Paragraph.objects.filter(writing__in=writings,pk=paragraph_id)
            serializer = ParagraphSerializer(paragraph)
            return Response(data=serializer.data,status=status.HTTP_200_OK)

    def patch(self,request):
        user = request.user

        writing_id = request.GET.get('writing_id', None)
        if writing_id is None:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        writing = get_object_or_404(Writing,writer=user,pk=writing_id)

        paragraph_id = request.GET.get('paragraph_id', None)
        if paragraph_id is None:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        paragraph = get_object_or_404(Paragraph,writing=writing,pk=paragraph_id)

        paragraph.bookmark = True if paragraph.bookmark==False else False
        paragraph.save()

        return Response(status=status.HTTP_200_OK)