import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk import word_tokenize

def slice_text(originals,translations):
    split_originals = re.split(r'[.\n]',originals) + '.'
    split_translations = re.split(r'[.\n]',translations) + '.'
    splitted_sentences = list(zip(split_originals,split_translations))
    
    res = []
    for original,translation in splitted_sentences:
        if (original.strip() and translation.strip()):
            res.append({
                "Original":original.strip(),
                "Translation":translation.strip()
            })
    return res

def make_feedback_all(text):
    res = []
    target_range = ['IN','MD','VB','VBD','VBG','VBN','VBP','VBZ']
    for sentence in text:
        original = sentence["Original"]
        translation = sentence["Translation"]
        target_words = []
        tags = nltk.pos_tag(word_tokenize(translation))
        for word,tag in tags:
            if tag in target_range:
                target_words.append(word)
        res.append({
                "Original":original,
                "Translation":translation,
                "TargetWord":str(target_words)
            })
    return res

def make_feedback_line(sentence):
    target_range = ['IN','MD','VB','VBD','VBG','VBN','VBP','VBZ']
    
    original = sentence["Original"]
    translation = sentence["Translation"]
    target_words = []
    tags = nltk.pos_tag(word_tokenize(translation))
    for word,tag in tags:
        if tag in target_range:
            target_words.append(word)
    return {
            "Original":original,
            "Translation":translation,
            "TargetWord":str(target_words)
        }

sentences = [
        {
            "Original": "응답의 우선순위를 정할 수 있으면 일회성 상호작용이든, 개별 Customer와 더 깊이 개별 고객과 더 깊이 연결할 수 있습니다",
            "Translation": "If you can determine the priority of responses, you can connect more deeply with individual customers, whether it's a one-time interaction or a deeper connection with individual customers"
        },
        {
            "Original": "특히 즐겁거나 화가 난 Experience에 대한 일회성 상호 작용 또는 Customer 기반 내에서 영향력 있는 User와 장기적인 Customer 기반 내에서 영향력 있는 개인과 장기적인 관계를 발전시킬 수 있습니다",
            "Translation": "You can develop relationships with influential users or long-term customers based on one-time interactions or customers based on loyalty"
        },
        {
            "Original": "다음과 같은 경우 브랜드, 제품 또는 서비스에 대해 호의적인 댓글을 게시한 적이 있는 경우",
            "Translation": "In cases where you have posted positive comments about a brand, product, or service"
        },
        {
            "Original": "브랜드, 제품 또는 서비스에 대해 호의적인 댓글을 게시한 적이 있다면, 그 댓글이 개인적으로 인정받는다면 어떤 기분이 들지 생각해 보세요",
            "Translation": "If you've posted positive comments about a brand, product, or service, think about how it would feel if those comments were personally acknowledged"
        },
        {
            "Original": "브랜드 매니저에게 인정받는다면 어떤 느낌일지 생각해 보세요",
            "Translation": "Think about how it would feel to be recognized by a brand manager"
        },
        {
            "Original": "일반적으로 사람들은 할 말이 있기 때문에 글을 게시하고 그 말을 한 것에 대해 인정받고 싶기 때문입니다",
            "Translation": "Generally, people want recognition for what they have said and posted, which is why they seek validation"
        },
        {
            "Original": "특히 다음과 같은 경우 사람들이 긍정적인 댓글을 게시하는 것은 감사의 표현입니다",
            "Translation": "Especially in cases where people post positive comments, it is an expression of gratitude"
        },
        {
            "Original": "반면 옆에 서 있는 사람에 대한 칭찬은 일반적으로 '감사합니다'와 같은 응답으로 답하지만, 안타까운 사실은 대부분의 브랜드 칭찬은 답장을 받지 못한다는 것입니다",
            "Translation": "On the other hand, praising someone standing next to you is usually responded to with a simple 'thank you,' but the unfortunate fact is that most brand compliments do not receive a response"
        },
        {
            "Original": "이러한 경우 불만을 유발한 원인을 칭찬의 동기가 무엇인지 이해하고 탄탄한 팬을 만들 수 있는 기회를 놓치게 됩니다",
            "Translation": "In such cases, missing the opportunity to understand the motivation behind the praise that sparked dissatisfaction and to create strong fans"
        }
    ]
print(make_feedback_all(sentences))