from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

conversation_summary_chain = ConversationChain(
    llm = llm,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2)
)

result = conversation_summary_chain.predict(input="嗨，你最近过的怎么样？")
conversation_summary_chain.predict(input="你最近学到什么新知识了?")
conversation_summary_chain.predict(input="你说1加1等于几？")

#__dict__:该对象的所有实例变量（attributes）
print(conversation_summary_chain.__dict__)



