from django.urls import path

from .views import *


urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view()),
    path('kakao/login/callback/', KakaoCallbackView.as_view()),
]