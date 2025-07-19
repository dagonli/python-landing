import numpy as np
import librosa
from scipy.spatial.distance import cosine, euclidean

class VoiceSimilarity:
    """纯Librosa语音相似度计算器，无深度学习依赖"""

    def __init__(self):
        """初始化参数"""
        self.sample_rate = 16000
        self.n_mfcc = 13  # MFCC系数数量
        self.n_fft = 2048  # FFT窗口大小
        self.hop_length = 512  # 帧移

    def load_audio(self, audio_file):
        """加载并预处理音频"""
        try:
            # 加载音频，自动重采样到16000Hz
            waveform, _ = librosa.load(audio_file, sr=self.sample_rate, mono=True)
            return waveform
        except Exception as e:
            raise RuntimeError(f"加载音频文件失败: {audio_file} - {str(e)}")

    def extract_features(self, audio_file):
        """提取音频的MFCC特征统计量"""
        waveform = self.load_audio(audio_file)

        # 提取MFCC特征
        mfcc = librosa.feature.mfcc(
            y=waveform,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )

        # 计算特征的统计量作为"声纹"
        mean = np.mean(mfcc, axis=1)
        std = np.std(mfcc, axis=1)
        max_vals = np.max(mfcc, axis=1)
        min_vals = np.min(mfcc, axis=1)

        # 组合所有统计量
        features = np.concatenate([mean, std, max_vals, min_vals])
        return features

    def compute_similarity(self, audio_file1, audio_file2, method="cosine"):
        """
        计算两个音频文件的相似度
        参数:
            audio_file1, audio_file2: 音频文件路径
            method: 相似度计算方法，"cosine"或"euclidean"
        返回:
            similarity: 相似度得分 (0-1范围，越高越相似)
        """
        # 提取特征
        feat1 = self.extract_features(audio_file1)
        feat2 = self.extract_features(audio_file2)

        # 计算相似度
        if method == "cosine":
            # 余弦相似度：[0, 1]，越接近1越相似
            # 使用1减去余弦距离得到相似度
            cos_sim = 1 - cosine(feat1, feat2)
            return max(0.0, cos_sim)  # 确保非负
        elif method == "euclidean":
            # 欧氏距离：越小越相似，转换为相似度得分
            distance = euclidean(feat1, feat2)
            # 使用指数函数转换为相似度 (0-1范围)
            return np.exp(-distance / 100)
        else:
            raise ValueError(f"不支持的相似度计算方法: {method}")


# 使用示例
if __name__ == "__main__":
    # 初始化相似度计算器
    similarity_calculator = VoiceSimilarity()
    print("语音相似度计算器已初始化")

    # 计算两个音频的相似度
    try:
        similarity = similarity_calculator.compute_similarity(
            "audio/client_1.wav",
            "audio/client_3.wav"
        )
        print(f"语音相似度: {similarity:.4f}")
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("可能原因：")
        print("1. 音频文件不存在或路径错误")
        print("2. 音频文件格式不支持")
        print("3. 音频文件过短（至少需要1秒以上）")
        print("4. 缺少依赖库，请确保安装了 librosa 和 numpy")