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

def parse_string_with_index_name(input_string):
    data = {'Ambiguity':'', 'Alternative':'', 'Nuance':''}
    print(input_string)
    ambiguity_index = input_string.find('[Task1]: ')
    alternative_index = input_string.find('[Task2]: ')
    nuance_index = input_string.find('[Task3]: ')
    data['Ambiguity'] = input_string[ambiguity_index+len('[Task1]: '):alternative_index].strip()
    data['Alternative'] = input_string[alternative_index+len('[Task2]: '):nuance_index].strip()
    data['Nuance'] = input_string[nuance_index+len('[Task3]: '):].strip()
    return data

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

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_feedback_line(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += """\
[Task0]: Task1,2,3에 대한 답변을 제외하고 다른 어떤 답변이나 인사도 하지마.
[Task1] : 밑의 Sentence에서 어색한 부분을 찾아서 한국어로 설명해줘.
[Task2]: 어색한 부분을 해결할 영문 대안을 제시해줘.
[Task3]: 원래의 문장과 어떤 점이 달라졌는지 뉘앙스를 한국어로 설명해줘.
[Senetence]: "%s"

Example Question ( for me ):
[Sentence]: "There were psychological studies in which subjects were shown photographs of people’s faces and asked to identify the expression or state of mind evinced."

Example Answer ( for you ):
[Task1]: 연구나 이론의 결과는 현재에도 영향이 있기 때문에 과거형 동사보다 현재완료형 동사가 어울립니다.
[Task2]: There were psychological studies in which subjects were shown photographs of people’s faces and asked to identify the expression or state of mind evinced.
[Task3]: 연구가 과거에만 존재하던 뉘앙스에서 벗어나, 연구가 진행되었다는 의미를 잘 보여줍니다.\
"""%data["Sentence"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response = openai_call_by_prompt(prompt)

    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    response_data = parse_string_with_index_name(response.data['Response'])
    response_data['Original'] = data["Sentence"]
    
    
    return Response(response_data)