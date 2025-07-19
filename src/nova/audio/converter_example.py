#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频转换工具使用示例
演示如何使用 AudioConverter 类将各种音频格式转换为 WAV 格式
"""

import os
import sys
from audio_converter import AudioConverter

def example_single_conversion():
    """
    单个文件转换示例
    """
    print("=== 单个文件转换示例 ===")
    
    # 创建转换器实例
    converter = AudioConverter(output_sample_rate=16000, output_channels=1)
    
    # 示例文件路径（请根据实际情况修改）
    input_file = input("请输入要转换的音频文件路径: ").strip()
    
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 {input_file}")
        return
    
    # 获取文件信息
    print(f"\n文件信息:")
    try:
        file_info = converter.get_file_info(input_file)
        print(f"文件名: {file_info['file_name']}")
        print(f"文件大小: {file_info['file_size']} 字节")
        print(f"文件格式: {file_info['file_extension']}")
        print(f"是否支持: {file_info['is_supported']}")
        
        if 'sample_rate' in file_info:
            print(f"采样率: {file_info['sample_rate']} Hz")
            print(f"时长: {file_info['duration']:.2f} 秒")
            print(f"声道数: {file_info['channels']}")
    except Exception as e:
        print(f"获取文件信息失败: {str(e)}")
        return
    
    # 执行转换
    print(f"\n开始转换...")
    result = converter.convert_to_wav(input_file)
    
    # 显示结果
    if result['status'] == 'success':
        print(f"转换成功!")
        print(f"输出文件: {result['output_path']}")
        print(f"使用方法: {result['used_method']}")
        print(f"输出采样率: {result['conversion_params']['sample_rate']} Hz")
        print(f"输出声道数: {result['conversion_params']['channels']}")
        
        # 显示输出文件信息
        output_info = result['output_file']
        print(f"输出文件大小: {output_info['file_size']} 字节")
        if 'duration' in output_info:
            print(f"输出时长: {output_info['duration']:.2f} 秒")
    else:
        print(f"转换失败: {result['error_message']}")

def example_batch_conversion():
    """
    批量转换示例
    """
    print("\n=== 批量转换示例 ===")
    
    # 创建转换器实例
    converter = AudioConverter(output_sample_rate=16000, output_channels=1)
    
    # 获取要转换的文件列表
    print("请输入要转换的音频文件路径（每行一个，输入空行结束）:")
    files = []
    while True:
        file_path = input().strip()
        if not file_path:
            break
        if os.path.exists(file_path):
            files.append(file_path)
        else:
            print(f"警告: 文件不存在 {file_path}")
    
    if not files:
        print("没有有效的文件")
        return
    
    # 获取输出目录
    output_dir = input("请输入输出目录（可选，直接回车使用当前目录）: ").strip()
    if not output_dir:
        output_dir = None
    elif not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        except Exception as e:
            print(f"创建输出目录失败: {str(e)}")
            return
    
    # 执行批量转换
    print(f"\n开始批量转换 {len(files)} 个文件...")
    result = converter.batch_convert(files, output_dir)
    
    # 显示结果
    print(f"\n批量转换完成:")
    print(f"总文件数: {result['total_files']}")
    print(f"成功转换: {result['successful_conversions']}")
    print(f"转换失败: {result['failed_conversions']}")
    
    # 显示详细结果
    print(f"\n详细结果:")
    for i, file_result in enumerate(result['results']):
        if file_result['status'] == 'success':
            print(f"  {i+1}. ✓ {os.path.basename(file_result['input_file']['file_path'])} -> {os.path.basename(file_result['output_path'])}")
        else:
            print(f"  {i+1}. ✗ {os.path.basename(file_result.get('input_path', 'unknown'))} - {file_result['error_message']}")

def example_different_formats():
    """
    不同格式转换示例
    """
    print("\n=== 不同格式转换示例 ===")
    
    # 创建转换器实例
    converter = AudioConverter(output_sample_rate=16000, output_channels=1)
    
    # 支持的格式列表
    supported_formats = list(converter.SUPPORTED_FORMATS.keys())
    print(f"支持的音频格式: {', '.join(supported_formats)}")
    
    # 测试文件转换
    test_files = []
    for ext in ['.mp3', '.flac', '.aac', '.ogg', '.m4a']:
        test_file = f"test{ext}"
        if os.path.exists(test_file):
            test_files.append(test_file)
    
    if test_files:
        print(f"\n发现测试文件: {test_files}")
        for test_file in test_files:
            print(f"\n转换 {test_file}:")
            result = converter.convert_to_wav(test_file)
            if result['status'] == 'success':
                print(f"  ✓ 成功转换")
            else:
                print(f"  ✗ 转换失败: {result['error_message']}")
    else:
        print("没有找到测试文件")

def example_custom_settings():
    """
    自定义设置示例
    """
    print("\n=== 自定义设置示例 ===")
    
    # 获取用户设置
    try:
        sample_rate = int(input("请输入目标采样率 (Hz，默认16000): ") or "16000")
        channels = int(input("请输入目标声道数 (1=单声道, 2=立体声，默认1): ") or "1")
    except ValueError:
        print("输入无效，使用默认设置")
        sample_rate = 16000
        channels = 1
    
    # 创建转换器实例
    converter = AudioConverter(output_sample_rate=sample_rate, output_channels=channels)
    
    print(f"转换器设置: 采样率={sample_rate}Hz, 声道数={channels}")
    
    # 执行转换
    input_file = input("请输入要转换的音频文件路径: ").strip()
    
    if os.path.exists(input_file):
        result = converter.convert_to_wav(input_file)
        if result['status'] == 'success':
            print(f"转换成功: {result['output_path']}")
        else:
            print(f"转换失败: {result['error_message']}")
    else:
        print("文件不存在")

def main():
    """
    主函数
    """
    print("音频文件转换工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 单个文件转换")
        print("2. 批量文件转换")
        print("3. 不同格式转换示例")
        print("4. 自定义设置转换")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            example_single_conversion()
        elif choice == '2':
            example_batch_conversion()
        elif choice == '3':
            example_different_formats()
        elif choice == '4':
            example_custom_settings()
        elif choice == '5':
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 