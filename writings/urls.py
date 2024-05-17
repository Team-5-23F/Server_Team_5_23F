from django.urls import path

from .views import *


app_name = 'writings'

urlpatterns = [
    path('writing/',WritingAPIView.as_view()),
    path('paragraph/', ParagraphListAPIView.as_view()),
]