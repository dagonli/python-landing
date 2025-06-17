from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain, SequentialChain
from langchain_core.prompts import PromptTemplate

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

# # 这是一个 LLMChain，根据剧名和设定的时代来撰写剧情简介。
template = """你是一位剧作家。根据戏剧的标题和设定的时代，你的任务是为该标题写一个简介。

标题：{title}
时代：{era}
剧作家：以下是对上述戏剧的简介："""

prompt_template = PromptTemplate(input_variables=["title","era"],template=template)
#output_key
synopsis_chain = LLMChain(llm=llm,prompt=prompt_template,output_key="synopsis",verbose=True)


# 这是一个LLMChain，用于根据剧情简介撰写一篇戏剧评论。
template = """你是《纽约时报》的戏剧评论家。根据该剧的剧情简介，你需要撰写一篇关于该剧的评论。

剧情简介：
{synopsis}

来自《纽约时报》戏剧评论家对上述剧目的评价："""

prompt_template = PromptTemplate(input_variables=["synopsis"],template=template)
review_chain = LLMChain(llm=llm,prompt=prompt_template,output_key="review",verbose=True)

m_overall_chain = SequentialChain(
    chains=[synopsis_chain,review_chain],
    input_variables=["title","era"],
    # here we return multiple variables
    output_variables=["synopsis","review"],
    verbose=True
)

result = m_overall_chain.invoke({"title":"三体人不是无法战胜的", "era": "二十一世纪的新中国"})

print(result)





