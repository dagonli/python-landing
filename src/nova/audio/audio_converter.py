#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频文件转换工具类
可以将任何音频格式转换为 WAV 格式
"""

import os
import sys
import logging
from pathlib import Path
import subprocess
import tempfile
import shutil
from typing import Optional, Tuple, Dict, Any

try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class AudioConverter:
    """
    音频文件转换器
    支持多种音频格式转换为 WAV 格式
    """
    
    # 支持的音频格式
    SUPPORTED_FORMATS = {
        # 常见音频格式
        '.mp3': 'MP3',
        '.wav': 'WAV',
        '.flac': 'FLAC',
        '.aac': 'AAC',
        '.ogg': 'OGG',
        '.wma': 'WMA',
        '.m4a': 'M4A',
        '.opus': 'OPUS',
        '.webm': 'WEBM',
        '.3gp': '3GP',
        '.amr': 'AMR',
        '.au': 'AU',
        '.aiff': 'AIFF',
        '.wv': 'WV',
        '.ape': 'APE',
        '.ra': 'RA',
        '.rm': 'RM',
        '.asf': 'ASF',
        '.avi': 'AVI',  # 视频文件中的音频
        '.mkv': 'MKV',  # 视频文件中的音频
        '.mp4': 'MP4',  # 视频文件中的音频
        '.mov': 'MOV',  # 视频文件中的音频
    }
    
    def __init__(self, output_sample_rate: int = 16000, output_channels: int = 1):
        """
        初始化音频转换器
        
        Args:
            output_sample_rate (int): 输出音频的采样率，默认16000Hz
            output_channels (int): 输出音频的声道数，默认1（单声道）
        """
        self.logger = logging.getLogger(__name__)
        self.output_sample_rate = output_sample_rate
        self.output_channels = output_channels
        
        # 检查可用的转换方法
        self.available_methods = []
        if LIBROSA_AVAILABLE:
            self.available_methods.append('librosa')
        if PYDUB_AVAILABLE:
            self.available_methods.append('pydub')
        
        self.logger.info(f"音频转换器初始化完成，可用方法: {self.available_methods}")
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        检查文件格式是否支持
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 是否支持该格式
        """
        if not os.path.exists(file_path):
            return False
        
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.SUPPORTED_FORMATS
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取音频文件信息
        
        Args:
            file_path (str): 音频文件路径
            
        Returns:
            dict: 文件信息字典
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            file_info = {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'file_extension': Path(file_path).suffix.lower(),
                'is_supported': self.is_supported_format(file_path)
            }
            
            # 如果支持该格式，尝试获取音频信息
            if file_info['is_supported'] and LIBROSA_AVAILABLE:
                try:
                    y, sr = librosa.load(file_path, sr=None, mono=False)
                    file_info.update({
                        'sample_rate': sr,
                        'duration': len(y) / sr,
                        'channels': y.shape[0] if len(y.shape) > 1 else 1,
                        'audio_data_shape': y.shape
                    })
                except Exception as e:
                    self.logger.warning(f"无法获取音频信息: {str(e)}")
            
            return file_info
            
        except Exception as e:
            self.logger.error(f"获取文件信息失败: {str(e)}")
            raise
    
    def convert_with_librosa(self, input_path: str, output_path: str) -> bool:
        """
        使用 librosa 转换音频文件
        
        Args:
            input_path (str): 输入文件路径
            output_path (str): 输出文件路径
            
        Returns:
            bool: 转换是否成功
        """
        try:
            if not LIBROSA_AVAILABLE:
                raise ImportError("librosa 未安装")
            
            # 加载音频文件
            y, sr = librosa.load(input_path, sr=self.output_sample_rate, mono=(self.output_channels == 1))
            
            # 保存为 WAV 格式
            sf.write(output_path, y.T if self.output_channels == 1 else y, self.output_sample_rate)
            
            self.logger.info(f"使用 librosa 成功转换: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"librosa 转换失败: {str(e)}")
            return False
    
    def convert_with_pydub(self, input_path: str, output_path: str) -> bool:
        """
        使用 pydub 转换音频文件
        
        Args:
            input_path (str): 输入文件路径
            output_path (str): 输出文件路径
            
        Returns:
            bool: 转换是否成功
        """
        try:
            if not PYDUB_AVAILABLE:
                raise ImportError("pydub 未安装")
            
            # 加载音频文件
            audio = AudioSegment.from_file(input_path)
            
            # 设置输出参数
            if self.output_channels == 1:
                audio = audio.set_channels(1)
            
            # 设置采样率
            audio = audio.set_frame_rate(self.output_sample_rate)
            
            # 导出为 WAV 格式
            audio.export(output_path, format="wav")
            
            self.logger.info(f"使用 pydub 成功转换: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"pydub 转换失败: {str(e)}")
            return False
    
    def convert_with_ffmpeg(self, input_path: str, output_path: str) -> bool:
        """
        使用 ffmpeg 转换音频文件（如果系统安装了 ffmpeg）
        
        Args:
            input_path (str): 输入文件路径
            output_path (str): 输出文件路径
            
        Returns:
            bool: 转换是否成功
        """
        try:
            # 检查 ffmpeg 是否可用
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                raise FileNotFoundError("ffmpeg 未安装或不可用")
            
            # 构建 ffmpeg 命令
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-ar', str(self.output_sample_rate),
                '-ac', str(self.output_channels),
                '-y',  # 覆盖输出文件
                output_path
            ]
            
            # 执行转换
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.logger.info(f"使用 ffmpeg 成功转换: {input_path} -> {output_path}")
                return True
            else:
                self.logger.error(f"ffmpeg 转换失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"ffmpeg 转换失败: {str(e)}")
            return False
    
    def convert_to_wav(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        将音频文件转换为 WAV 格式
        
        Args:
            input_path (str): 输入音频文件路径
            output_path (str, optional): 输出 WAV 文件路径，如果为None则自动生成
            
        Returns:
            dict: 转换结果信息
        """
        try:
            # 检查输入文件
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"输入文件不存在: {input_path}")
            
            # 获取文件信息
            file_info = self.get_file_info(input_path)
            
            if not file_info['is_supported']:
                raise ValueError(f"不支持的音频格式: {file_info['file_extension']}")
            
            # 生成输出路径
            if output_path is None:
                input_name = Path(input_path).stem
                output_path = f"{input_name}_converted.wav"
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 尝试不同的转换方法
            conversion_success = False
            used_method = None
            
            # 方法1: 使用 librosa
            if 'librosa' in self.available_methods:
                if self.convert_with_librosa(input_path, output_path):
                    conversion_success = True
                    used_method = 'librosa'
            
            # 方法2: 使用 pydub
            if not conversion_success and 'pydub' in self.available_methods:
                if self.convert_with_pydub(input_path, output_path):
                    conversion_success = True
                    used_method = 'pydub'
            
            # 方法3: 使用 ffmpeg
            if not conversion_success:
                if self.convert_with_ffmpeg(input_path, output_path):
                    conversion_success = True
                    used_method = 'ffmpeg'
            
            if not conversion_success:
                raise RuntimeError("所有转换方法都失败了")
            
            # 获取输出文件信息
            output_info = self.get_file_info(output_path)
            
            result = {
                'status': 'success',
                'input_file': file_info,
                'output_file': output_info,
                'used_method': used_method,
                'output_path': output_path,
                'conversion_params': {
                    'sample_rate': self.output_sample_rate,
                    'channels': self.output_channels
                }
            }
            
            self.logger.info(f"音频转换成功: {input_path} -> {output_path} (使用 {used_method})")
            return result
            
        except Exception as e:
            self.logger.error(f"音频转换失败: {str(e)}")
            return {
                'status': 'error',
                'error_message': str(e),
                'input_path': input_path,
                'output_path': output_path
            }
    
    def batch_convert(self, input_files: list, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        批量转换音频文件
        
        Args:
            input_files (list): 输入文件路径列表
            output_dir (str, optional): 输出目录，如果为None则使用当前目录
            
        Returns:
            dict: 批量转换结果
        """
        results = {
            'total_files': len(input_files),
            'successful_conversions': 0,
            'failed_conversions': 0,
            'results': []
        }
        
        for input_file in input_files:
            try:
                if output_dir:
                    filename = Path(input_file).stem + '.wav'
                    output_path = os.path.join(output_dir, filename)
                else:
                    output_path = None
                
                result = self.convert_to_wav(input_file, output_path)
                results['results'].append(result)
                
                if result['status'] == 'success':
                    results['successful_conversions'] += 1
                else:
                    results['failed_conversions'] += 1
                    
            except Exception as e:
                self.logger.error(f"批量转换失败 {input_file}: {str(e)}")
                results['failed_conversions'] += 1
                results['results'].append({
                    'status': 'error',
                    'error_message': str(e),
                    'input_path': input_file
                })
        
        self.logger.info(f"批量转换完成: {results['successful_conversions']}/{results['total_files']} 成功")
        return results


def main():
    """
    主函数 - 用于测试和演示
    """
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建转换器
    converter = AudioConverter(output_sample_rate=16000, output_channels=1)
    
    print("音频文件转换工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 转换单个文件")
        print("2. 批量转换文件")
        print("3. 查看文件信息")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == '1':
            # 单个文件转换
            input_file = input("请输入音频文件路径: ").strip()
            if os.path.exists(input_file):
                result = converter.convert_to_wav(input_file)
                if result['status'] == 'success':
                    print(f"转换成功: {result['output_path']}")
                else:
                    print(f"转换失败: {result['error_message']}")
            else:
                print("文件不存在")
        
        elif choice == '2':
            # 批量转换
            print("请输入音频文件路径（每行一个，输入空行结束）:")
            files = []
            while True:
                file_path = input().strip()
                if not file_path:
                    break
                if os.path.exists(file_path):
                    files.append(file_path)
                else:
                    print(f"文件不存在: {file_path}")
            
            if files:
                output_dir = input("请输入输出目录（可选）: ").strip()
                if not output_dir:
                    output_dir = None
                
                result = converter.batch_convert(files, output_dir)
                print(f"批量转换完成: {result['successful_conversions']}/{result['total_files']} 成功")
        
        elif choice == '3':
            # 查看文件信息
            input_file = input("请输入音频文件路径: ").strip()
            if os.path.exists(input_file):
                try:
                    info = converter.get_file_info(input_file)
                    print(f"文件信息: {info}")
                except Exception as e:
                    print(f"获取文件信息失败: {str(e)}")
            else:
                print("文件不存在")
        
        elif choice == '4':
            print("退出程序")
            break
        
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main() 