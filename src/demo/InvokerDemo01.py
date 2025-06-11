import requests

# 接口地址
url = "https://stg1-btl-front-web.daikuan.360.cn/llm/handler/agent/geo/query"

# 请求头，设置 Content-Type 为 JSON
headers = {
    "Content-Type": "application/json"
}

# 请求参数
data = {
    "location": "114.029331,22.52658"
}

try:
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 判断请求是否成功
    if response.status_code == 200:
        print("请求成功，返回结果：")
        print(response.json())
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print("响应内容：", response.text)
except Exception as e:
    print("请求出错：", e)
