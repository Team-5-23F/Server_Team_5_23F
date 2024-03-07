from django.http import JsonResponse 
from openai import OpenAI
from config.settings import env

client = OpenAI(api_key=env('OPENAI_KEY'))

def get_gpt_response(prompt):
    # print("prompt: ",prompt)
    
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role':'user',
                    'content':prompt
                },
            ],
            max_tokens=1024
        )
    except:
        # print('OpenAI API is not working')
        return None

    # print(response.choices[0].message.content)

    return response.choices[0].message.content