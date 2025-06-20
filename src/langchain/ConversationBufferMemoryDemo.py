from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

conversation_chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory = ConversationBufferMemory()
)

result = conversation_chain.predict(input = "你是谁？")

print(result)

result1= conversation_chain.predict(input="你和马云有啥关系吗？")
print(result1)