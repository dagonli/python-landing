import  os

from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent, AgentType

from src.langchain.llm_model_util import get_model

#设置自己的Serp API key
os.environ["SERP_API_KEY"]="106c03a3b52f0c1803b012cae572c33b8d642f29414132a8a113e54888eadd69"


llm = get_model("qwen3-32b")


#实例化工具
search = SerpAPIWrapper(serpapi_api_key="106c03a3b52f0c1803b012cae572c33b8d642f29414132a8a113e54888eadd69")
tools= [
    Tool(
        name ="Intermediate Answer",
        func = search.run,
        description="useful for when you need to ask with search",
    )
]


# tools: Sequence[BaseTool],
# llm: BaseLanguageModel,
# agent: Optional[AgentType] = None,
#实例化 SELF_ASK_WITH_SEARCH agent
self_ask_with_search_Agent = initialize_agent(tools,llm,agent=AgentType.SELF_ASK_WITH_SEARCH,verbose=True)

self_ask_with_search_Agent.invoke("2025年NBA总决赛冠军和MVP分别是谁？")


# Reason-only 错误：非启发式 Prompt（容易出现事实类错误，未结合 Web Search 工具）
print(llm.invoke("2023年大运会举办地在哪里？"))
