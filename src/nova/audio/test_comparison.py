#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频比对功能测试脚本
"""

import os
import sys
from example_usage import example_all_files_comparison

def main():
    """
    主函数
    """
    print("音频比对功能测试")
    print("=" * 50)
    
    # 默认分析files目录
    target_dir = 'files'
    if not os.path.isdir(target_dir):
        print(f"错误: 未找到目录 {target_dir}")
        return
    
    # 检查files目录下的音频文件
    audio_files = []
    for ext in ['.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a']:
        audio_files.extend([f for f in os.listdir(target_dir) if f.lower().endswith(ext)])
    print(f"{target_dir} 目录下找到 {len(audio_files)} 个音频文件:")
    for i, file in enumerate(audio_files, 1):
        print(f"  {i}. {file}")
    if len(audio_files) < 2:
        print("错误: 至少需要2个音频文件才能进行测试")
        return
    # 运行比对分析
    print(f"\n开始运行音频比对分析...")
    example_all_files_comparison(target_dir)
    print("\n测试完成!")

if __name__ == "__main__":
    main() 