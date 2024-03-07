from django.urls import path
from .views import *

app_name = 'apis'

urlpatterns = [ 
    path('gpt/outline/', openai_outline, name='gpt_outline'),
    path('gpt/translate/', openai_translate, name='gpt_translate'),
]