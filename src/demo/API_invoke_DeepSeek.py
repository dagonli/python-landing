# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-1c5d3c7af76f4962ae3e3ed6e0d8741c", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个资深股票操盘手。"},
        {"role": "user", "content": "深度分析下，今天京北方的股价走势及后续策略？"},
    ],
    stream=False
)

print(response.choices[0].message.content)