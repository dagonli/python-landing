# -*- coding: utf-8 -*-
import os
import base64
import json
import dotenv

dotenv.load_dotenv()

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

# 音频文件路径
SOURCE_AUDIO_PATH = r"audio\client_1.wav"  # 源音频文件
DEST_AUDIO_PATH = r"audio\client_2.wav"  # 目标音频文件（示例使用相同文件）

try:
    # 读取音频文件并转换为Base64
    def load_audio_base64(file_path):
        with open(file_path, 'rb') as audio_file:
            return base64.b64encode(audio_file.read()).decode('utf-8')


    # 加载凭证
    # cred = credential.Credential(
    #     os.getenv("TENCENTCLOUD_SECRET_ID"),
    #     os.getenv("TENCENTCLOUD_SECRET_KEY")
    # )

    # 加载凭证
    cred = credential.Credential(
        "xxx",
        "xx"
    )


    # 配置HTTP和客户端
    httpProfile = HttpProfile()
    httpProfile.endpoint = "asr.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = asr_client.AsrClient(cred, "ap-guangzhou", clientProfile)

    # 准备请求参数
    req = models.VoicePrintCompareRequest()
    params = {
        "SrcAudioData": load_audio_base64(SOURCE_AUDIO_PATH),
        "DestAudioData": load_audio_base64(DEST_AUDIO_PATH),
        "VoiceFormat": 1,  # 1表示wav格式
        "SampleRate": 16000  # 采样率必须与音频实际采样率一致
    }
    req.from_json_string(json.dumps(params))

    # 发送请求
    resp = client.VoicePrintCompare(req)
    print("比对结果：")
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(f"API调用失败: {err}")
except FileNotFoundError as err:
    print(f"音频文件不存在: {err}")
except Exception as err:
    print(f"发生未知错误: {err}")