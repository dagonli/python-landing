from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

prompt = PromptTemplate(
    input_variables=["product"],
    template="给{product}讲1个简单的笑话",
)

chain = LLMChain(llm=llm, prompt=prompt)


chain.verbose =True
print(chain.invoke({
    'product': "程序员"
}))