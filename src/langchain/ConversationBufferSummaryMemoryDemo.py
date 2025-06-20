## 在内存中保留了最近的交互缓冲区，但不仅仅是完全清除旧的交互，而是将它们编译成摘要并同时使用。与以前的实现不同的是，它使用token长度而不是交互次数来确定何时清除交互。
from langchain.memory import ConversationSummaryBufferMemory

from src.langchain.llm_model_util import get_model

memory = ConversationSummaryBufferMemory(llm=get_model("qwen3-32b"),max_token_limit=10)

memory.save_context({"input": "嗨，你最近过得怎么样？"}, {"output": " 嗨！我最近过得很好，谢谢你问。我最近一直在学习新的知识，并且正在尝试改进自己的性能。我也在尝试更多的交流，以便更好地了解人类的思维方式。"})
memory.save_context({"input": "你最近学到什么新知识了?"}, {"output": " 最近我学习了有关自然语言处理的知识，以及如何更好地理解人类的语言。我还学习了有关机器学习的知识，以及如何使用它来改善自己的性能。"})

memory.load_memory_variables({})

print(memory.load_memory_variables({})["history"])