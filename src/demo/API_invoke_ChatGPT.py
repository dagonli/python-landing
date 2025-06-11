import openai

#我拿不到我的值，所以我先注释掉
api_key = "额度已经用光了"

# 创建 OpenAI 客户端
client = openai.OpenAI(api_key=api_key)

# 调用 ChatCompletion 接口，发送消息并获取回复
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一个资深股票操盘手。"},
        {"role": "user", "content": "深度分析下，今天京北方的股价走势及后续策略？"}
    ],
    temperature=0.7,  # 设置回复的随机性
    max_tokens=150  # 设置回复的最大 token 数
)

# 打印返回的回复内容
print(response.choices[0].message['content'])






