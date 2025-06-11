import requests
import json

# 接口地址
url = "http://10.224.150.60/v1/chat/completions"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer qwen3-32b"
}

# 请求数据
data = {
    "model": "qwen3-32b",
    "messages": [
        {
            "role": "user",
            "content": "不要解释过程，直接给出结果。你是谁？"
        }
    ],
    "extra_body": {
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
}

try:
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 判断请求是否成功
    if response.status_code == 200:
        print("请求成功，返回结果：")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print("响应内容：", response.text)

except Exception as e:
    print("请求出错：", e)
