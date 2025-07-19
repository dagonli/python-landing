import os
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import logging

class AudioSimilarityAnalyzer:
    """
    音频相似度分析器
    使用 resemblyzer 工具类来判断两个音频文件的相似度
    """
    
    def __init__(self, model_path=None):
        """
        初始化音频相似度分析器
        
        Args:
            model_path (str, optional): 预训练模型路径，如果为None则使用默认模型
        """
        self.logger = logging.getLogger(__name__)
        self.encoder = VoiceEncoder(model_path)
        self.logger.info("音频相似度分析器初始化完成")
    
    def load_audio(self, audio_path):
        """
        加载并预处理音频文件
        
        Args:
            audio_path (str): 音频文件路径
            
        Returns:
            numpy.ndarray: 预处理后的音频数据
        """
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"音频文件不存在: {audio_path}")
            
            # 检查文件格式
            if not audio_path.lower().endswith('.wav'):
                raise ValueError(f"只支持WAV格式音频文件: {audio_path}")
            
            # 使用 resemblyzer 预处理音频
            wav = preprocess_wav(Path(audio_path))
            self.logger.info(f"成功加载音频文件: {audio_path}")
            return wav
            
        except Exception as e:
            self.logger.error(f"加载音频文件失败 {audio_path}: {str(e)}")
            raise
    
    def extract_embedding(self, audio_data):
        """
        提取音频的嵌入向量
        
        Args:
            audio_data (numpy.ndarray): 预处理后的音频数据
            
        Returns:
            numpy.ndarray: 音频嵌入向量
        """
        try:
            # 使用 resemblyzer 提取嵌入向量
            embedding = self.encoder.embed_utterance(audio_data)
            self.logger.info("成功提取音频嵌入向量")
            return embedding
            
        except Exception as e:
            self.logger.error(f"提取音频嵌入向量失败: {str(e)}")
            raise
    
    def calculate_similarity(self, embedding1, embedding2):
        """
        计算两个嵌入向量的相似度
        
        Args:
            embedding1 (numpy.ndarray): 第一个音频的嵌入向量
            embedding2 (numpy.ndarray): 第二个音频的嵌入向量
            
        Returns:
            float: 相似度分数 (0-1之间，1表示完全相同)
        """
        try:
            # 计算余弦相似度
            similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
            self.logger.info(f"计算相似度完成: {similarity:.4f}")
            return float(similarity)
            
        except Exception as e:
            self.logger.error(f"计算相似度失败: {str(e)}")
            raise
    
    def compare_audio_files(self, audio_path1, audio_path2):
        """
        比较两个音频文件的相似度
        
        Args:
            audio_path1 (str): 第一个音频文件路径
            audio_path2 (str): 第二个音频文件路径
            
        Returns:
            dict: 包含相似度分数和详细信息的字典
        """
        try:
            self.logger.info(f"开始比较音频文件: {audio_path1} 和 {audio_path2}")
            
            # 加载音频文件
            audio1 = self.load_audio(audio_path1)
            audio2 = self.load_audio(audio_path2)
            
            # 提取嵌入向量
            embedding1 = self.extract_embedding(audio1)
            embedding2 = self.extract_embedding(audio2)
            
            # 计算相似度
            similarity_score = self.calculate_similarity(embedding1, embedding2)
            
            # 返回结果
            result = {
                'audio1_path': audio_path1,
                'audio2_path': audio_path2,
                'similarity_score': similarity_score,
                'similarity_percentage': similarity_score * 100,
                'status': 'success'
            }
            
            self.logger.info(f"音频相似度分析完成: {similarity_score:.4f} ({similarity_score*100:.2f}%)")
            return result
            
        except Exception as e:
            self.logger.error(f"音频相似度分析失败: {str(e)}")
            return {
                'audio1_path': audio_path1,
                'audio2_path': audio_path2,
                'similarity_score': None,
                'similarity_percentage': None,
                'status': 'error',
                'error_message': str(e)
            }
    
    def get_similarity_description(self, similarity_score):
        """
        根据相似度分数返回描述性文本
        
        Args:
            similarity_score (float): 相似度分数
            
        Returns:
            str: 相似度描述
        """
        if similarity_score >= 0.9:
            return "极高相似度 - 很可能是同一个人的声音"
        elif similarity_score >= 0.8:
            return "高相似度 - 可能是同一个人的声音"
        elif similarity_score >= 0.7:
            return "中等相似度 - 可能是相似的声音特征"
        elif similarity_score >= 0.5:
            return "低相似度 - 声音特征有一定差异"
        else:
            return "极低相似度 - 声音特征差异很大"


def main():
    """
    主函数 - 用于测试和调试
    """
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建音频相似度分析器
    analyzer = AudioSimilarityAnalyzer()
    
    # 测试音频文件路径
    audio1_path = "胡亚军1.wav"
    audio2_path = "李豫1.wav"
    
    # 检查文件是否存在
    if not os.path.exists(audio1_path):
        print(f"错误: 音频文件不存在 {audio1_path}")
        return
    
    if not os.path.exists(audio2_path):
        print(f"错误: 音频文件不存在 {audio2_path}")
        return
    
    # 比较音频文件
    result = analyzer.compare_audio_files(audio1_path, audio2_path)
    
    # 输出结果
    print("\n=== 音频相似度分析结果 ===")
    print(f"音频文件1: {result['audio1_path']}")
    print(f"音频文件2: {result['audio2_path']}")
    
    if result['status'] == 'success':
        print(f"相似度分数: {result['similarity_score']:.4f}")
        print(f"相似度百分比: {result['similarity_percentage']:.2f}%")
        print(f"相似度描述: {analyzer.get_similarity_description(result['similarity_score'])}")
    else:
        print(f"分析失败: {result.get('error_message', '未知错误')}")


if __name__ == "__main__":
    main() 