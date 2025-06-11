from zhipuai import ZhipuAI
import sys
client = ZhipuAI(api_key="cb63520e04d44a04c1cae90cfcdafcc6.uTkSHpw9iACxmBgf")
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {
            "role": "user",
            "content": ""
        }
    ],
    top_p=0.7,
    temperature=0.9,
    stream=True,
    max_tokens=2000,
)

if response:
    for chunk in response:
        #每次输出都会在同一行的末尾添加，并且在输出后立即刷新缓冲区，从而立即看到结果。
        sys.stdout.write(chunk.choices[0].delta.content)
        sys.stdout.flush()
    print()