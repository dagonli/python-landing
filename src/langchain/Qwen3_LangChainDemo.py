from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
import requests
import json

from .llm_model_util import get_model


llm = get_model("qwen3-32b")

# 直接调用模型
print(llm.invoke("给我讲1个简短的程序员笑话"))


# 流式输出结果
try:
    for chunk in llm.stream([HumanMessage(content="讲一个简短的程序员笑话，不要输出思考过程")]):
        print(chunk.content, end="", flush=True)
except Exception as e:
    print(f"请求超时或出错: {e}")
