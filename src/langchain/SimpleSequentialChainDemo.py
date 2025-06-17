from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain_core.prompts import PromptTemplate

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

title_template = """你是一位剧作家。根据戏剧的标题，你的任务是为该标题写一个简介。

标题：{title}
剧作家：以下是对上述戏剧的简介："""

prompt_template = PromptTemplate(input_variables=["title"], template=title_template)
synopsis_chain = LLMChain(llm=llm, prompt = prompt_template)
synopsis_chain.verbose =True

# print(synopsis_chain.invoke(
#     {"title":"央视新闻"}
# ))

synopsis_template ="""你是一个算数专家，你的工作是为算出这个给出的标题，有多少个汉字。

剧情简介：
{synopsis}

以下是来自你计算之后的字数统计："""
synopsis_prompt_template = PromptTemplate(input_variables=["synopsis"], template=synopsis_template)
review_chain = LLMChain(llm=llm, prompt = synopsis_prompt_template)

# 这是一个SimpleSequentialChain，按顺序运行这两个链
overall_chain = SimpleSequentialChain(chains=[synopsis_chain,review_chain],verbose=True)

review = overall_chain.invoke("星球大战第九季")


