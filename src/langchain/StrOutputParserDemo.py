#### The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 1.0. Use :meth:`~RunnableSequence, e.g., `prompt | llm`` instead.
#### 【新增】langchain 0.3版本，使用RunnableSequence替换LLMChain，并指定 output_key
#### pip show langchain 查看版本命令
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from src.langchain.llm_model_util import get_model

llm = get_model("qwen3-32b")

summarizing_prompt_template = """
总结以下文本为一个 20 字以内的句子:
---
{content}
"""

summarizing_prompt = PromptTemplate.from_template(summarizing_prompt_template)
summarizing_chain = summarizing_prompt | llm | StrOutputParser()

translating_prompt_template = """
将{summary}翻译成英文:
"""
translating_prompt = PromptTemplate.from_template(translating_prompt_template)
translating_chain = translating_prompt | llm | StrOutputParser()

# Construct a RunnableSequence with custom output keys
overall_chain = summarizing_chain | {
    'summary':summarizing_chain,
    'translation':translating_chain
}



test_contetent = """
端到端在深度学习中指的是一种模型架构设计理念：
从原始输入数据到最终输出结果，整个决策过程完全由单一神经网络完成，无需人工设计中间处理环节。
这种设计摒弃了传统分步骤、模块化的处理流程，让模型自主挖掘数据中隐藏的复杂关联。
"""



result = overall_chain.invoke({"content":test_contetent})

print(result)




