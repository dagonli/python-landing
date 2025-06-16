from langchain.output_parsers import DatetimeOutputParser
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from src.langchain.llm_model_util import get_model

output_parser= DatetimeOutputParser()

template = """Answer the users question:

{question}

{format_instructions}"""

prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)

print(prompt)

print(prompt.format(question="around when was bitcoin founded?"))

llm=get_model("qwen3-32b")
chain = prompt | llm
output = chain.invoke("around when was bitcoin founded?")
print(output)


output_after_parser = output_parser.parse(output.content)
print(output_after_parser)




