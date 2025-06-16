from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain.schema import (AIMessage,HumanMessage,SystemMessage)
import requests
import json

from langchain_core.prompts import PromptTemplate

from .llm_model_util import get_model


llm = get_model("qwen3-32b")


prompt_template = PromptTemplate.from_template(
    "给我讲{nums}个简短的程序员笑话"
)

prompt= prompt_template.format(nums=2)

# 直接调用模型
print(llm.invoke(prompt))


# 流式输出结果
try:
    for chunk in llm.stream([HumanMessage(content="讲一个简短的程序员笑话，不要输出思考过程")]):
        print(chunk.content, end="", flush=True)
except Exception as e:
    print(f"请求超时或出错: {e}")


messages =[
    SystemMessage(content="你是一个资深股票分析师"),
    HumanMessage(content="A股市值最高的股票是哪个？"),
    AIMessage(content="是贵州茅台"),
    HumanMessage(content="它是在哪个省份的公司？")
]

print(messages)

chat_result = llm.invoke(messages)

print(chat_result)

print(type(chat_result))


