
from resemblyzer import preprocess_wav, VoiceEncoder

from pathlib import Path
import numpy as np
import base64
import wave
import json

def recognize(audio_data:str) -> str:

    # 把audioData进行base64解码
    audio_data = base64.b64decode(audio_data)
    pcm_to_wav(audio_data, 'D:\\pyproject\\test\\音频识别\\temp.wav')

    # 加载语音编码器模型
    encoder = VoiceEncoder()

    input_temp_path = Path("D:\\pyproject\\test\\音频识别\\temp.wav")
    staff_path = Path("D:\\pyproject\\test\\音频识别\\test6_1.wav")
    customer_path = Path("D:\\pyproject\\test\\音频识别\\test4_1.wav")
    
    temp_wav = preprocess_wav(input_temp_path)
    staff_wav = preprocess_wav(staff_path)
    customer_wav = preprocess_wav(customer_path)
    
    # 获取语音嵌入
    temp_v = encoder.embed_utterance(temp_wav)
    staff_v = encoder.embed_utterance(staff_wav)
    customer_v = encoder.embed_utterance(customer_wav)
    
    # 计算相似度
    staff_similarity = np.dot(staff_v, temp_v) / (np.linalg.norm(staff_v) * np.linalg.norm(temp_v))
    print(f"staff similarity: {staff_similarity}")

    customer_similarity = np.dot(customer_v, temp_v) / (np.linalg.norm(customer_v) * np.linalg.norm(temp_v))
    print(f"customer similarity: {customer_similarity}")

    speaker = 1
    if customer_similarity > staff_similarity:
        speaker = 2

    return json.dumps({
        "staff_similarity": float(staff_similarity),
        "customer_similarity": float(customer_similarity),
        "speaker": speaker
    })

def pcm_to_wav(pcm_data, output_path, channels=1, sample_width=2, frame_rate=16000):
    """
    将PCM数据转换为WAV文件。

    :param pcm_data: PCM数据
    :param output_path: 输出WAV文件路径
    :param channels: 声道数，默认1（单声道）
    :param sample_width: 采样宽度，默认2（16位）
    :param frame_rate: 采样率，默认16000
    """
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(pcm_data)

# 示例用法
# with open('input.pcm', 'rb') as pcm_file:
#     pcm_data = pcm_file.read()

# pcm_to_wav(pcm_data, 'output.wav')