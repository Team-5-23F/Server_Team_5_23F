from django.urls import path

from .views import *


app_name = 'writings'

urlpatterns = [
    path('detail/',WritingAPIView.as_view()),
    path('list/', WritingListAPIView.as_view()),
    path('paragraph/', ParagraphListAPIView.as_view()),
]