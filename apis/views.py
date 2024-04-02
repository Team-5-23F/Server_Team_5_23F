import json
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from GPT.views import get_gpt_response
from rest_framework.permissions import IsAuthenticated

def parse_string_with_index_number(input_string):
    print(input_string)
    lines = input_string.split('\n')
    parsed_data = []
    for line in lines:
        if len(line)==0: continue
        if '0'>line[0] or '9'<line[0]:
            continue
        index_of_first_space = line.find(' ')
        if index_of_first_space != -1:
            parsed_data.append(line[index_of_first_space+1:])

    return parsed_data

def openai_call_by_prompt(prompt):
    try:
        openai_response = get_gpt_response(prompt)
    except:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({'Response': openai_response})

@api_view(('POST',))
@permission_classes([IsAuthenticated])
def openai_translate(request):
    prompt = ""
    try:
        prompt = json.loads(request.body)["Text"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    prompt += """1. translate the text that follows the input, without omitting anything.\n\
            2. Translate Korean proper nouns as they are pronounced, without paraphrasing.\n\n\
            """+str(prompt)
    response = openai_call_by_prompt(prompt)
    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response({'Text':response.data['Response']})

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_outline(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += "[Task]: 자세한 설명이나 이유를 생략하고, %s를 작성하는 글의 형식을 제공해줘.\n"%data["Task"]
        prompt += "[Context] : %s인 상황이야\n"%data["Context"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
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

    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response({'Index': parse_string_with_index_number(response.data['Response'])})