from langchain.prompts import ChatPromptTemplate

from src.langchain.llm_model_util import get_model

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

# 生成提示
messages = template.format_messages(
    name="Dagon",
    user_input="What is your name?"
)

print(messages[0].content)
print(messages[-2].content)


# 调用模型生成问答
llm = get_model("qwen3-32b")

print(llm.invoke(messages))
