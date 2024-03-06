from django.http import JsonResponse 
import openai
from config.settings import env

def get_gpt_response(prompt):
    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role':'user',
                'content':prompt
            }
        ],
        max_token=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = query.choices[0].message["content"]
    return response