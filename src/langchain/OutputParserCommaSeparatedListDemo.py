from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import OpenAI

from src.langchain.llm_model_util import get_model

# 创建一个输出解析器，用于处理带逗号分隔的列表输出
output_parser = CommaSeparatedListOutputParser()

# 获取格式化指令，该指令告诉模型如何格式化其输出
format_instructions = output_parser.get_format_instructions()

# 创建一个提示模板，它会基于给定的模板和变量来生成提示
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",  # 模板内容
    input_variables=["subject"],  # 输入变量
    partial_variables={"format_instructions": format_instructions}  # 预定义的变量，这里我们传入格式化指令
)

# 使用提示模板和给定的主题来格式化输入
_input=prompt.format(subject="ice cream falvors")

print(_input)


llm = get_model("qwen3-32b")
output = llm.invoke(_input)
print(output)

# 使用之前创建的输出解析器来解析模型的输出
print(output_parser.parse(output.content))