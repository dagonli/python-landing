import hashlib
import json

def sort_json_dict(obj):
    # "递归排序JSON对象中的所有字典”
    if isinstance(obj, dict):
        return {k: sort_json_dict(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        return [sort_json_dict(item) for item in obj]
    return obj

def md5_salt(password, salt):
    # 创建 MD5 对象
    md5_hash = hashlib.md5()
    # 将密码与盐进行拼接
    salted_password = password + salt
    # 更新哈希对象
    md5_hash.update(salted_password.encode('utf-8'))
    # 获取加密后的密码
    encrypted_password = md5_hash.hexdigest()
    return encrypted_password


def main(userId: str, robotId: str, bizdata: str) -> dict:
    json_object = {
        "bizData": bizdata,
        "robotId": robotId,
        "operatorUserId": userId
    }
    # 递归排序JSON对象
    sorted_json_object = sort_json_dict(json_object)
    # 将排序后的字典转换为JSON字符串，不包含多余的空格
    json_string = json.dumps(sorted_json_object, separators=(',', ':'), ensure_ascii=False)

    return {
        "sign": md5_salt(json_string, "be891eea444f4cc598a646874cb9258c")
    }

result = main("123", "123", "123")
print(result)