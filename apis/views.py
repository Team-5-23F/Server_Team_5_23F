import json
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from GPT.views import get_gpt_response
from NE.views import *
from rest_framework.permissions import IsAuthenticated

def parse_string_with_index_number(index_list):
    ret = []
    # print(index_list)
    # index_list = eval(index_list)
    # for index in index_list:
    #     ret.append(index.value)
    return ret

def parse_string_with_index_name(original, input):
    input = eval(input)
    data = [original,input["Task1"].strip(), input["Task2"].strip(),input["Task3"].strip()]
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
    original = ""
    try:
        original = json.loads(request.body)["Text"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    prompt = """[Task] Translate the Korean+English text, without omitting anything.\n\
        [Input]: Korean or English Text\n\
        [Output]: English Text\n\
        [Requirements] Translate Korean proper nouns as they are pronounced, without paraphrasing.\n\n\
        [Text]: """+str(original)
    response = openai_call_by_prompt(prompt)
    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    translated = response.data['Response']

    splitted = slice_text(original,translated)
    return Response({
        "Text":translated,
        "Result":splitted,
    },status=status.HTTP_200_OK)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_outline(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += "[Task]: 자세한 설명이나 이유를 생략하고, %s를 작성하는 글의 단락별 아웃라인을 json 형식으로 제공해줘.\n"%data["Task"]
        prompt += "[Context] : %s인 상황이야\n"%data["Context"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    prompt += """[Example] : 
    Example Question ( for me ):
    [Task]: 메일을 작성하는 글의 단락별 형식을 제공해줘
    [Context]: 개인면담요청인 상황이야
    
    Example Answer ( for you ):
    {
        "para1":"인삿말",
        "para2":"자기소개",
        "para3":"요청사항",
        "para4":"요청사유",
        "para5":"끝인사"
    }"""

    response = openai_call_by_prompt(prompt)

    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    index_paragraph = eval(response.data['Response'])
    return Response({"NumOfIndex":len(index_paragraph),"Index":index_paragraph})

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_feedback_line(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += """\
[Description]: 하단에 오는 딕셔너리의 리스트는 Original에서 Translation으로 번역된 문장이야.  Task1,2,3에 대한 답변을 한국말로 Json 형식으로 제공해줘. 이때 어떠한 인삿말이나 부가 적인 답변은 필요 없어.
[Task1] : Translation에서 Original과 비교했을 때 같은 의미를 전달하지 못하는 부분을 찾아 지적해줘.
[Task2]: Translation과 같은 의미를 갖는 다른 문장을 제시해줘.
[Task3]: 원래의 문장과 어떤 점이 달라졌는지 뉘앙스의 차이를 설명해줘.

Example Question ( for me ):
{
    "Original": "응답의 우선순위를 정할 수 있으면 일회성 상호작용이든, 개별 Customer와 더 깊이 개별 고객과 더 깊이 연결할 수 있습니다",
    "Translation": "If you can prioritize responses, you can deepen individual connections with individual customers, whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions",
}

Example Answer ( for you ):
{
    "Sentence":"If you can prioritize responses, you can deepen individual connections with individual customers, whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions",
    "Task1": "Translation에서 '개별 Customer와 더 깊이 개별 고객과 더 깊이 연결할 수 있습니다' 부분이 'whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions'로 번역되면서 '영향력 있는 사용자와의 장기적인 관계'라는 의미가 추가되었습니다. Original에는 이런 내용이 없습니다.",
    "Task2": "If you can prioritize responses, you can deepen individual connections with customers, whether it's a one-time interaction or not.",
    "Task3": "번역된 문장은 원래 문장에 없는 '영향력 있는 사용자와의 장기적인 관계'라는 내용을 추가하여, 의미가 다소 변경되었습니다. 원래 문장은 일회성 상호작용이든 장기적인 관계든 상관없이 개별 고객과 깊이 연결할 수 있다는 것을 강조하고 있습니다."
}


""" + str(data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response = openai_call_by_prompt(prompt)

    if response.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    response_data = eval(response.data['Response'])
    
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def openai_feedback_all(request):
    data = json.loads(request.body)
    prompt = ""
    try:
        prompt += """\
[Description]: 하단에 오는 딕셔너리의 리스트는 Original에서 Translation으로 문장별로 번역된 글이야. TargetWord를 중심으로 Task1,2,3에 대한 답변을 한국말로 Json 형식으로 제공해줘. 이때 어떠한 인삿말이나 부가 적인 답변은 필요 없어.
[Task1] : 문장에서 TargetWord를 중심으로 어색한 부분을 찾아 지적해줘.
[Task2]: 어색한 부분을 해소한 개선된 문장을 제시해줘.
[Task3]: 원래의 문장과 어떤 점이 달라졌는지 뉘앙스의 차이를 설명해줘.


Example Question ( for me ):
[
    {
        "Original": "응답의 우선순위를 정할 수 있으면 일회성 상호작용이든, 개별 Customer와 더 깊이 개별 고객과 더 깊이 연결할 수 있습니다",
        "Translation": "If you can prioritize responses, you can deepen individual connections with individual customers, whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions",
        "TargetWord": "['If', 'can', 'prioritize', 'can', 'deepen', 'with', 'whether', \"'s\", 'with', 'based', 'on']"
    },
    {
        "Original": "특히 즐겁거나 화가 난 Experience에 대한 일회성 상호 작용 또는 Customer 기반 내에서 영향력 있는 User와 장기적인 Customer 기반 내에서 영향력 있는 개인과 장기적인 관계를 발전시킬 수 있습니다",
        "Translation": "In particular, you can develop influential relationships with individuals and long-term customers based on one-time interactions or customers' experiences of joy or anger",
        "TargetWord": "['In', 'can', 'develop', 'with', 'based', 'on', 'of']"
    },
    ...
]

Example Answer ( for you ):
[
    {
        "Sentence":"If you can prioritize responses, you can deepen individual connections with individual customers, whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions",
        "Task1": "'you can deepen individual connections with individual customers' 문장에서 'individual'이 반복 사용되어 어색하고, 'whether it's a one-time interaction or a long-term relationship with influential users based on customer interactions' 문장이 어색하게 구성되어 있습니다.",
        "Task2": "If you can prioritize responses, you can deepen connections with customers, whether it's a one-time interaction or a long-term relationship based on customer interactions.",
        "Task3": "수정된 문장은 'individual'의 반복을 제거하고 문장의 구조를 단순화하여 더 명확하고 읽기 쉽게 만들었습니다."
    },
    {
        "Sentence": "In particular, you can develop influential relationships with individuals and long-term customers based on one-time interactions or customers' experiences of joy or anger",
        "Task1": "'일회성 상호 작용 또는 Customer 기반 내에서 영향력 있는 User와 장기적인 Customer 기반 내에서 영향력 있는 개인과 장기적인 관계' 문장이 어색하고 반복적으로 사용되고 있습니다.",
        "Task2": "In particular, you can develop influential relationships with individuals and long-term customers based on one-time interactions or impactful experiences.",
        "Task3": "수정된 문장은 중복을 제거하고 문장을 간결하게 하여 전반적인 가독성과 흐름을 개선했습니다."
    },
    ...
]



"""+str(make_feedback_all(data["Writing"]))
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    response_data = openai_call_by_prompt(prompt)

    if response_data.status_code is not status.HTTP_200_OK:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    response = json.loads(response_data.data["Response"])
    return Response(response,status=status.HTTP_200_OK)