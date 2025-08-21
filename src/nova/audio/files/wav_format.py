import wave
import os

# 替换为你的文件路径
file_path = "C:\\Users\\liyu-jk\\Desktop\\线下AI获客助手\\第二期\\trimmer\\test111.wav"






with wave.open(file_path, "rb") as wf:
    # 检查文件是否存在
    if os.path.exists(file_path):
        print("文件存在")
    else:
        print("文件不存在")


    print("声道数:", wf.getnchannels())
    print("采样宽度（位深度）:", wf.getsampwidth() * 8, "bit")
    print("采样率:", wf.getframerate(), "Hz")
    print("帧数:", wf.getnframes())
    print("编码格式:", wf.getcomptype(), wf.getcompname())