from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from .lib.permission import *

user_retrieve_response = openapi.Response('', UserInfoSerializer)

class UserView(APIView):
    permission_classes = [AllowAny]

    def get_or_create_user(self, data: dict):
        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data
        serializer.create(validated_data=user)

        return Response(data=user, status=status.HTTP_201_CREATED)
    
    def post(self, request):
        '''
        회원 정보
        or 회원가입 ( 등록 )
        '''
        return self.get_or_create_user(data=request.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def object(self, data: dict):
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data

        return Response(data=user, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        로그인
        '''
        return self.object(data=request.data)
    

class LogoutView(APIView):
    permission_classes = [LoginRequired]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        '''
        로그아웃
        '''
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data.blacklist()

        return Response(status=status.HTTP_202_ACCEPTED)
    

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        '''
        Token 재발급
        '''
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data

        return Response(data=token, status=status.HTTP_201_CREATED)


class UserInfoView(APIView):
    '''
    회원 정보
    '''
    permission_classes = [LoginRequired]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        '''
        회원 정보 조회
        'social_id', 'social_type', 'email', 'created_at', 'last_login'
        '''
        serializer = UserInfoSerializer(request.user)
        response_data = serializer.data

        return Response(data=response_data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=UserInfoSerializer, response={200:''})
    def patch(self, request, *args, **kwargs):
        '''
        회원 정보 수정
        '''
        data = request.data

        serializer = UserInfoSerializer(request.user, data=data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        '''
        회원 탈퇴
        '''
        request.user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)