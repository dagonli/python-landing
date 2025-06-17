from typing import TypeAlias

from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_qwq import ChatQwQ

from ..common.logger import log

ModelT: TypeAlias = (
        ChatOpenAI
        | ChatQwQ
        | ChatDeepSeek
)


def get_model(model_name) -> ModelT:
    llm_config = {
        "default_llm": "jarvis-turbo",
        "default_agent": "qwen3-32b",
        "list": [
            {
                "model": "jarvis-turbo",
                "api_key": "dify-dev-jarvis-turbo",
                "base_url": "http://jarvis-llm.daikuan.qihoo.net/v1",
                "temperature": 0.7,
                "max_tokens": 8000
            },
            {
                "model": "qwen2.5-72b",
                "api_key": "qwen2.5-72b",
                "base_url": "http://10.224.150.60/v1",
                "temperature": 0.7,
                "max_tokens": 20000
            },
            {
                "model": "qwq-32b",
                "api_key": "qwq-32b",
                "base_url": "http://10.224.150.60/v1/chat/completions",
                "temperature": 0.7,
                "max_tokens": 20000,
                "request_timeout":3
            },
            {
                "model": "qwen3-32b",
                "api_key": "qwen3-32b",
                "base_url": "http://10.224.150.60/v1",
                "temperature": 0.7,
                "max_tokens": 20000,
                "request_timeout":120
            },
            {
                "model": "Qwen/Qwen3-14B",
                "api_key": "Qwen/Qwen3-14B ",
                "base_url": "http://10.228.131.53/v1",
                "temperature": 0.7,
                "max_tokens": 20000,
                "request_timeout":10
            }
        ]
    }
    llm_list = llm_config.get("list") or []
    res_llm_config_list = [item for item in llm_list if item["model"] == model_name]
    res_llm_config = res_llm_config_list[0]
    if not model_name or not res_llm_config:
        res_llm_config.setdefault('temperature', 0.7)
        res_llm_config.setdefault('max_tokens', 20000)
        res_llm_config.setdefault('top_p', 0.9)
        model_name = llm_config.get("default_llm") or 'jarvis-turbo'

    log(f"get_model model_name={model_name}, res_llm_config={res_llm_config}")

    if model_name in ['qwq-32b']:
        return ChatQwQ(
            api_base=res_llm_config.get('base_url'),
            **res_llm_config
        )

    if model_name in ['deepseek']:
        return ChatDeepSeek(
            api_base=res_llm_config.get('base_url'),
            **res_llm_config
        )
    return ChatOpenAI(**res_llm_config)


print(get_model("qwen3-32b"))