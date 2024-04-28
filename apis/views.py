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
[Task1] : 밑의 Sentence에서 조동사, 시제, 그리고 전치사를 위주로 어색한 부분을 찾아서 영어로 제시하고 이유를 한글로 설명해줘.
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
    
    
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_feedback_all(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += """\
[Task0]: '[Writing]'을 문장별로 나누어서 Task1,2,3에 대한 답변을 Json 형식으로 제공해줘. 이때 어떠한 인삿말이나 부가 적인 답변은 필요 없어.
[Task1] : 문장에서 어색한 부분을 찾아 지적해줘.
[Task2]: 어색한 부분을 해소한 개선된 문장을 제시해줘.
[Task3]: 원래의 문장과 어떤 점이 달라졌는지 뉘앙스의 차이를 설명해줘.
[Writing]: "%s"

Example Question ( for me ):
[Writing]: "If you can prioritize responses, you can deepen connections with individual customers, whether through one-off interactions or through more meaningful connections. Especially in cases where customers have posted favorable comments about a brand, product, or service. Think about how you would feel if your comment was personally acknowledged. And imagine how it would feel to be acknowledged by a brand manager. Generally, people post comments because they want their words to be acknowledged. Particularly when people post positive comments, it is an expression of gratitude. On the other hand, it is a sad fact that most brand compliments go unanswered. In such cases, missing the opportunity to understand the motivation behind the praise may lead to generating dissatisfaction, ultimately missing the chance to create loyal fans."

Example Answer ( for you ):
[
{
“Sentence1”: "If you can prioritize responses, you can deepen connections with individual customers, whether through one-off interactions or through more meaningful connections.”,
“Task1”: “문장의 흐름이 약간 어색한데, "whether through one-off interactions or through more meaningful connections" 부분이 더 자연스럽게 통일되어야 합니다.”,
“Task2”: "By prioritizing responses, you can deepen connections with individual customers, whether through one-off interactions or through more substantial engagements.”,
“Task3”: “수정된 문장은 구문의 일관성을 높이고, "substantial engagements"를 통해 보다 의미 있는 상호 작용에 대한 강조를 더합니다.”
},
{
“Sentence2”: “Especially in cases where customers have posted favorable comments about a brand, product, or service.”,
“Task1”: “문장에서 "Especially in cases where"로 시작하는 부분이 조금 어색합니다.”,
“Task2”: "Particularly when customers have posted favorable comments about a brand, product, or service.”,
“Task3”: “원래의 문장은 특정 상황을 강조하려는 의도였지만, 수정된 문장은 보다 자연스럽게 그 강조를 전달합니다.”
},
…
]\
"""%data["Writing"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response_data = openai_call_by_prompt(prompt)

    if response_data.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    response = json.loads(response_data.data["Response"])
    return Response(response,status=status.HTTP_200_OK)