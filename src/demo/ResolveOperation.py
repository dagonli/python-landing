import regex

def main(llm_result) -> dict:
    # 判断llm_result中是否有json串，有提取出来

    llm_result_valid_json = _extract_valid_json(llm_result)

    if llm_result_valid_json :
        llm_result_json = json.loads(llm_result_valid_json)
        biz_data = llm_result_json.get('biz_data')
        if biz_data:
            llm_result_json['biz_data'] = json.dumps(biz_data, ensure_ascii=False)
        else :
            llm_result_json['biz_data'] = '{}'
        return {
            **llm_result_json,
            'response':''
        }
    else :
        return {
            'response':llm_result,
            'biz_data':'',
            'method':'',
            'operator_type':'RESPONSE_DIRECT'
        }

def _extract_valid_json(llm_result):
    # 正则表达式匹配整个JSON对象，包括嵌套对象
    json_pattern = r'\{[^{}]*(?:(?R)[^{}]*)*\}'
    # 使用regex.search来匹配字符串中的JSON部分
    match = regex.search(json_pattern, llm_result)

    if match:
        json_str = match.group(0)
        fixed_json_str = fix_json_string(json_str)
        return fixed_json_str if _is_valid_json(fixed_json_str) else None
    else:
        return None

def fix_json_string(json_str):
    # 将所有单引号替换为双引号
    json_str = json_str.replace("'", '"')

    # 修复字符串数组中的引号
    def fix_array(match):
        array_str = match.group(0)
        # 将数组中的双引号替换为单引号，然后将整个数组的单引号替换回双引号
        fixed_array_str = regex.sub(r'"', "'", array_str)
        fixed_array_str = regex.sub(r"'([^']*)'", r'"\1"', fixed_array_str)
        return fixed_array_str

    # 使用正则表达式匹配字符串数组
    return regex.sub(r'\[.*?\]', fix_array, json_str)

def _is_valid_json(json_string):
    try:
        json_object = json.loads(json_string)  # 尝试解析字符串为JSON
        return True  # 解析成功，返回True
    except json.JSONDecodeError:  # 解析失败，捕获异常
        return False  # 返回False，表示不是有效的JSON格式