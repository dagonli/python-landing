from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
import requests
import json

from .llm_model_util import get_model


class CustomQwenChat(BaseChatModel):
    base_url: str = "http://10.224.150.60/v1/chat/completions"
    model_name: str = "qwen3-32b"
    api_key: str = "qwen3-32b"
    temperature: float = 0.7
    max_tokens: int = 1024

    def _generate(self, messages: list[BaseMessage], **kwargs) -> ChatResult:
        # 构造请求数据
        payload = {
            "model": self.model_name,
            "messages": [{"role": msg.type, "content": msg.content} for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "extra_body": {
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        }

        # 请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 发送请求
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

        # 解析响应
        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # 返回结果
        generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "custom_qwen"

llm = get_model("qwen3-32b")


async def method1(self):
    async for chunk in llm.astream([
        {"role": "system", "content": "讲一个程序员笑话"}
    ]):
        print(chunk.content)


    # 初始化模型
qwen_model = CustomQwenChat()

# 构造输入消息
# messages = [HumanMessage(content="讲一个程序员笑话")]




# 调用模型
# result = qwen_model.invoke(messages)

# 输出结果
# print(result.content)