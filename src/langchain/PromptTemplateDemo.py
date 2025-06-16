from langchain import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
)

# 使用 format 生成提示
prompt = prompt_template.format(adjective="funny", content="my son")
print(prompt)


print(prompt_template)

prompt_template = PromptTemplate.from_template(
    "Tell me a joke"
)
# 生成提示
prompt = prompt_template.format()
print(prompt)