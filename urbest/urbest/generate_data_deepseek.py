import jieba.posseg as pseg
from openai import OpenAI
from os import environ


KEYWORDS_CACHE = {}
client = OpenAI(api_key=environ.get("deepseek_sk"), base_url="https://api.deepseek.com")

def generate_data(for_what: str) -> None:
    """Generate data using DeepSeek API."""
    try:
        keywords = get_import_word(for_what)
        if keywords in KEYWORDS_CACHE.keys():
            return KEYWORDS_CACHE[keywords]
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个鼓励师,你需要按照我的要求生成对应的夸奖语言的列表,比如我需要你夸奖我羽毛球,你就回复我`你打球像林丹|你快把对面杀穿了|你的反手棒极了`列表长度30条且以|作为分隔符,并且不要在前面设置编号,严格遵循我的格式要求"},
                {"role": "user", "content": f"鼓励我与`{for_what}`相关的内容"},
            ],
            stream=False
        )
        data = response.choices[0].message.content.split('|')
        KEYWORDS_CACHE[keywords] = data
        print(KEYWORDS_CACHE)
    except Exception as e:
        print(f"Error generating data: {e}")
        data = ["出错了，请稍后再试。"]
    return data


def get_import_word(sentence: str) -> set:
    words_pos = pseg.cut(sentence)
    keywords = [x for x, flag in words_pos if flag in ('n', 'l', 'a', 'eng')]
    return tuple(keywords)

if __name__ == "__main__":
    data = generate_data("很nice的人")
    print(data)