import json
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,renderer_classes
from rest_framework import status
from GPT.views import get_gpt_response

def parse_string_with_newlines(input_string):
    lines = input_string.split('\n')
    parsed_data = []

    for line in lines:
        index_of_first_space = line.find(' ')
        if index_of_first_space != -1:
            parsed_data.append(line[index_of_first_space+1:])

    return parsed_data

def openai_call_by_prompt(prompt):
    try:
        openai_response = get_gpt_response(prompt)
    except:
        return Response({'Response':'OpenAI Server is not working'},status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'Response': openai_response})

@api_view(('POST',))
def openai_translate(request):
    prompt = json.loads(request.body)["prompt"]
    prompt = """1. translate the text that follows the input, without omitting anything.\n\
            2. Translate Korean proper nouns as they are pronounced, without paraphrasing.\n\n\
            """+str(prompt)
    return openai_call_by_prompt(prompt)

@api_view(['POST',])
def openai_outline(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += "[Task]: 자세한 설명이나 이유를 생략하고, %s를 작성하는 글의 형식을 제공해줘.\n"%data["Task"]
        prompt += "[Context] : %s인 상황이야\n"%data["Context"]
    except:
        return Response({'Response':'Body Type is not valid'},status=status.HTTP_400_BAD_REQUEST)
    
    prompt += """[Example] : 
    Q. "[Task]: 메일을 작성하는 글의 형식을 제공해줘
    [Context]: 개인면담요청인 상황이야"
    A.
    "1. 인삿말
    2.자기소개
    3.요청사항
    4.요청사유
    5.끝인사"""


    response = openai_call_by_prompt(prompt)
    response.data['Response'] = parse_string_with_newlines(response.data['Response'])
    
    return response