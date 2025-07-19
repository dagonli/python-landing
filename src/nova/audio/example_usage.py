#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频相似度分析使用示例
演示如何使用 AudioSimilarityAnalyzer 类来比较两个音频文件的相似度
"""

import os
import sys
import glob
import tempfile
import re
from datetime import datetime
from audio_similarity import AudioSimilarityAnalyzer
from audio_converter import AudioConverter

# 尝试导入pandas和openpyxl用于Excel输出
try:
    import pandas as pd
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

def extract_name_from_filename(filename):
    """
    从文件名中提取姓名
    
    Args:
        filename (str): 文件名
        
    Returns:
        str: 提取的姓名，如果无法提取则返回None
    """
    # 移除文件扩展名
    name_without_ext = os.path.splitext(filename)[0]
    
    # 尝试提取中文姓名（2-4个中文字符）
    chinese_name_pattern = r'[\u4e00-\u9fff]{2,4}'
    chinese_matches = re.findall(chinese_name_pattern, name_without_ext)
    
    if chinese_matches:
        # 返回第一个匹配的中文姓名
        return chinese_matches[0]
    
    # 如果没有中文姓名，尝试提取英文姓名
    # 匹配连续的英文字母（可能包含空格）
    english_name_pattern = r'[a-zA-Z\s]+'
    english_matches = re.findall(english_name_pattern, name_without_ext)
    
    if english_matches:
        # 清理并返回英文姓名
        english_name = english_matches[0].strip()
        if len(english_name) >= 2:  # 至少2个字符
            return english_name
    
    return None

def analyze_comparison_logic(file1_name, file2_name, similarity_score, status):
    """
    分析比对逻辑，判断是否为特殊情况
    
    Args:
        file1_name (str): 第一个文件名
        file2_name (str): 第二个文件名
        similarity_score (float): 相似度分数
        status (str): 比对状态
        
    Returns:
        str: 逻辑分析结果
    """
    if status != 'success' or similarity_score is None:
        return ''
    
    # 提取姓名
    name1 = extract_name_from_filename(file1_name)
    name2 = extract_name_from_filename(file2_name)
    
    if not name1 or not name2:
        return ''
    
    # 判断姓名是否相同
    names_same = name1 == name2
    
    # 判断相似度等级
    if similarity_score >= 0.7:
        similarity_level = "中等以上"
    elif similarity_score >= 0.5:
        similarity_level = "中等"
    else:
        similarity_level = "低"
    
    # 逻辑判断
    if names_same and similarity_score < 0.7:
        return "同一个人比对失败"
    elif not names_same and similarity_score >= 0.7:
        return "不同人相似度高"
    
    return ''

def example_basic_usage():
    """
    基本使用示例
    """
    print("=== 基本使用示例 ===")
    
    # 创建分析器实例
    analyzer = AudioSimilarityAnalyzer()
    
    # 音频文件路径
    audio1 = "client_1.wav"
    audio2 = "client_2.wav"
    
    # 检查文件是否存在
    if not os.path.exists(audio1) or not os.path.exists(audio2):
        print("错误: 请确保 client_1.wav 和 client_2.wav 文件存在")
        return
    
    # 比较音频文件
    result = analyzer.compare_audio_files(audio1, audio2)
    
    # 显示结果
    print(f"音频1: {result['audio1_path']}")
    print(f"音频2: {result['audio2_path']}")
    
    if result['status'] == 'success':
        print(f"相似度: {result['similarity_score']:.4f}")
        print(f"相似度百分比: {result['similarity_percentage']:.2f}%")
        print(f"描述: {analyzer.get_similarity_description(result['similarity_score'])}")
    else:
        print(f"分析失败: {result.get('error_message', '未知错误')}")

def example_custom_paths():
    """
    自定义路径示例
    """
    print("\n=== 自定义路径示例 ===")
    
    # 创建分析器实例
    analyzer = AudioSimilarityAnalyzer()
    
    # 让用户输入音频文件路径
    audio1 = input("请输入第一个音频文件路径: ").strip()
    audio2 = input("请输入第二个音频文件路径: ").strip()
    
    # 检查文件是否存在
    if not os.path.exists(audio1):
        print(f"错误: 文件不存在 {audio1}")
        return
    
    if not os.path.exists(audio2):
        print(f"错误: 文件不存在 {audio2}")
        return
    
    # 比较音频文件
    result = analyzer.compare_audio_files(audio1, audio2)
    
    # 显示结果
    print(f"\n分析结果:")
    print(f"音频1: {result['audio1_path']}")
    print(f"音频2: {result['audio2_path']}")
    
    if result['status'] == 'success':
        print(f"相似度: {result['similarity_score']:.4f}")
        print(f"相似度百分比: {result['similarity_percentage']:.2f}%")
        print(f"描述: {analyzer.get_similarity_description(result['similarity_score'])}")
    else:
        print(f"分析失败: {result.get('error_message', '未知错误')}")

def example_batch_analysis():
    """
    批量分析示例
    """
    print("\n=== 批量分析示例 ===")
    
    # 创建分析器实例
    analyzer = AudioSimilarityAnalyzer()
    
    # 音频文件列表
    audio_files = [
        "client_1.wav",
        "client_2.wav"
    ]
    
    # 检查文件是否存在
    existing_files = []
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            existing_files.append(audio_file)
        else:
            print(f"警告: 文件不存在 {audio_file}")
    
    if len(existing_files) < 2:
        print("错误: 至少需要2个音频文件才能进行比较")
        return
    
    # 进行两两比较
    print(f"将对 {len(existing_files)} 个音频文件进行两两比较:")
    for i, file1 in enumerate(existing_files):
        for j, file2 in enumerate(existing_files[i+1:], i+1):
            print(f"\n比较 {file1} 和 {file2}:")
            
            result = analyzer.compare_audio_files(file1, file2)
            
            if result['status'] == 'success':
                print(f"  相似度: {result['similarity_score']:.4f} ({result['similarity_percentage']:.2f}%)")
                print(f"  描述: {analyzer.get_similarity_description(result['similarity_score'])}")
            else:
                print(f"  分析失败: {result.get('error_message', '未知错误')}")

def convert_audio_to_wav_if_needed(audio_path, converter):
    """
    如果需要，将音频文件转换为WAV格式
    
    Args:
        audio_path (str): 音频文件路径
        converter (AudioConverter): 音频转换器实例
        
    Returns:
        str: WAV文件路径（如果转换成功）或原始路径
    """
    if audio_path.lower().endswith('.wav'):
        return audio_path
    
    try:
        # 创建临时文件
        temp_dir = tempfile.mkdtemp()
        temp_wav_path = os.path.join(temp_dir, f"temp_{os.path.basename(audio_path)}.wav")
        
        # 转换音频文件
        result = converter.convert_to_wav(audio_path, temp_wav_path)
        
        if result['status'] == 'success':
            print(f"  已转换 {audio_path} -> {temp_wav_path}")
            return temp_wav_path
        else:
            print(f"  转换失败 {audio_path}: {result.get('error_message', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"  转换异常 {audio_path}: {str(e)}")
        return None

def example_all_files_comparison(target_dir=None):
    """
    比对指定目录下所有音频文件并输出格式化表格
    Args:
        target_dir (str): 目标目录，默认为None（当前目录），如果为None则自动用'files'目录
    """
    print("\n=== 所有音频文件比对分析 ===")
    
    # 目录处理
    if target_dir is None:
        if os.path.isdir('files'):
            target_dir = 'files'
        else:
            target_dir = '.'
    print(f"分析目录: {os.path.abspath(target_dir)}")
    
    # 创建分析器和转换器实例
    analyzer = AudioSimilarityAnalyzer()
    converter = AudioConverter(output_sample_rate=16000, output_channels=1)
    
    # 获取目标目录下所有音频文件
    audio_extensions = ['*.wav', '*.mp3', '*.flac', '*.aac', '*.ogg', '*.m4a']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(target_dir, ext)))
    audio_files = [f for f in audio_files if os.path.isfile(f)]
    
    if len(audio_files) < 2:
        print(f"错误: {target_dir} 目录下至少需要2个音频文件才能进行比较")
        print(f"找到的音频文件: {audio_files}")
        return
    
    print(f"找到 {len(audio_files)} 个音频文件:")
    for i, file in enumerate(audio_files, 1):
        print(f"  {i}. {file}")
    
    # 转换非WAV格式的音频文件
    print(f"\n检查并转换非WAV格式的音频文件...")
    converted_files = []
    temp_files = []
    for audio_file in audio_files:
        if audio_file.lower().endswith('.wav'):
            converted_files.append(audio_file)
        else:
            converted_path = convert_audio_to_wav_if_needed(audio_file, converter)
            if converted_path:
                converted_files.append(converted_path)
                if converted_path != audio_file:
                    temp_files.append(converted_path)
            else:
                print(f"  跳过 {audio_file} (转换失败)")
    if len(converted_files) < 2:
        print("错误: 转换后至少需要2个有效的音频文件才能进行比较")
        return
    print(f"转换后共有 {len(converted_files)} 个有效音频文件")
    
    # 进行两两比较并收集结果
    comparison_results = []
    total_comparisons = len(converted_files) * (len(converted_files) - 1) // 2
    current_comparison = 0
    print(f"\n开始进行 {total_comparisons} 次两两比较...")
    for i, file1 in enumerate(converted_files):
        for j, file2 in enumerate(converted_files[i+1:], i+1):
            current_comparison += 1
            original_file1 = audio_files[i] if i < len(audio_files) else file1
            original_file2 = audio_files[j] if j < len(audio_files) else file2
            print(f"进度: {current_comparison}/{total_comparisons} - 比较 {os.path.basename(original_file1)} 和 {os.path.basename(original_file2)}")
            result = analyzer.compare_audio_files(file1, file2)
            
            # 分析比对逻辑
            logic_analysis = analyze_comparison_logic(
                os.path.basename(original_file1),
                os.path.basename(original_file2),
                result.get('similarity_score'),
                result['status']
            )
            
            comparison_results.append({
                'file1': os.path.basename(original_file1),
                'file2': os.path.basename(original_file2),
                'file1_path': original_file1,
                'file2_path': original_file2,
                'similarity_score': result.get('similarity_score'),
                'similarity_percentage': result.get('similarity_percentage'),
                'status': result['status'],
                'error_message': result.get('error_message', ''),
                'description': analyzer.get_similarity_description(result.get('similarity_score', 0)) if result.get('similarity_score') is not None else 'N/A',
                'logic_analysis': logic_analysis
            })
    print_formatted_table(comparison_results)
    if temp_files:
        print(f"\n清理临时文件...")
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    temp_dir = os.path.dirname(temp_file)
                    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                        os.rmdir(temp_dir)
            except Exception as e:
                print(f"  清理临时文件失败 {temp_file}: {str(e)}")

def print_formatted_table(results):
    """
    输出格式化的表格对比结果
    
    Args:
        results (list): 比对结果列表
    """
    print("\n" + "="*140)
    print("音频文件相似度对比结果表")
    print("="*140)
    
    # 表头
    header = f"{'序号':<4} {'文件1':<20} {'文件2':<20} {'相似度分数':<12} {'相似度百分比':<12} {'相似度描述':<30} {'状态':<8} {'逻辑分析':<20}"
    print(header)
    print("-" * 140)
    
    # 表格内容
    for i, result in enumerate(results, 1):
        file1_name = result['file1'][:18] + ".." if len(result['file1']) > 20 else result['file1']
        file2_name = result['file2'][:18] + ".." if len(result['file2']) > 20 else result['file2']
        
        if result['status'] == 'success':
            similarity_score = f"{result['similarity_score']:.4f}" if result['similarity_score'] is not None else "N/A"
            similarity_percentage = f"{result['similarity_percentage']:.2f}%" if result['similarity_percentage'] is not None else "N/A"
            description = result['description'][:28] + ".." if len(result['description']) > 30 else result['description']
            status = "成功"
        else:
            similarity_score = "N/A"
            similarity_percentage = "N/A"
            description = "转换失败"
            status = "失败"
        
        # 逻辑分析
        logic_analysis = result.get('logic_analysis', '')[:18] + ".." if len(result.get('logic_analysis', '')) > 20 else result.get('logic_analysis', '')
        
        row = f"{i:<4} {file1_name:<20} {file2_name:<20} {similarity_score:<12} {similarity_percentage:<12} {description:<30} {status:<8} {logic_analysis:<20}"
        print(row)
    
    print("-" * 140)
    
    # 统计信息
    successful_comparisons = sum(1 for r in results if r['status'] == 'success')
    failed_comparisons = len(results) - successful_comparisons
    
    # 逻辑分析统计
    logic_analysis_count = sum(1 for r in results if r.get('logic_analysis'))
    same_person_failures = sum(1 for r in results if r.get('logic_analysis') == '同一个人比对失败')
    different_person_high_similarity = sum(1 for r in results if r.get('logic_analysis') == '不同人相似度高')
    
    print(f"统计信息:")
    print(f"  总比较次数: {len(results)}")
    print(f"  成功比较: {successful_comparisons}")
    print(f"  失败比较: {failed_comparisons}")
    print(f"  逻辑分析标识: {logic_analysis_count}")
    print(f"    同一个人比对失败: {same_person_failures}")
    print(f"    不同人相似度高: {different_person_high_similarity}")
    
    if successful_comparisons > 0:
        # 找出最高和最低相似度
        valid_results = [r for r in results if r['status'] == 'success' and r['similarity_score'] is not None]
        if valid_results:
            max_similarity = max(valid_results, key=lambda x: x['similarity_score'])
            min_similarity = min(valid_results, key=lambda x: x['similarity_score'])
            
            print(f"  最高相似度: {max_similarity['similarity_score']:.4f} ({max_similarity['file1']} vs {max_similarity['file2']})")
            print(f"  最低相似度: {min_similarity['similarity_score']:.4f} ({min_similarity['file1']} vs {min_similarity['file2']})")
    
    print("="*140)
    
    # 保存结果到Excel文件
    save_results_to_excel(results)

def save_results_to_excel(results):
    """
    将比对结果保存到Excel文件
    
    Args:
        results (list): 比对结果列表
    """
    if not EXCEL_AVAILABLE:
        print("警告: pandas 未安装，无法生成Excel文件")
        save_results_to_file(results)
        return
    
    try:
        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_similarity_results_{timestamp}.xlsx"
        
        # 准备数据
        data = []
        for i, result in enumerate(results, 1):
            data.append({
                '序号': i,
                '文件1': result['file1'],
                '文件2': result['file2'],
                '文件1路径': result['file1_path'],
                '文件2路径': result['file2_path'],
                '相似度分数': result['similarity_score'] if result['similarity_score'] is not None else 'N/A',
                '相似度百分比': f"{result['similarity_percentage']:.2f}%" if result['similarity_percentage'] is not None else 'N/A',
                '相似度描述': result['description'],
                '状态': '成功' if result['status'] == 'success' else '失败',
                '错误信息': result['error_message'] if result['status'] != 'success' else '',
                '逻辑分析': result.get('logic_analysis', '')
            })
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 创建Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 写入主要数据表
            df.to_excel(writer, sheet_name='比对结果', index=False)
            
            # 获取工作表对象以进行格式化
            worksheet = writer.sheets['比对结果']
            
            # 调整列宽
            column_widths = {
                'A': 8,   # 序号
                'B': 25,  # 文件1
                'C': 25,  # 文件2
                'D': 40,  # 文件1路径
                'E': 40,  # 文件2路径
                'F': 15,  # 相似度分数
                'G': 15,  # 相似度百分比
                'H': 35,  # 相似度描述
                'I': 10,  # 状态
                'J': 30,  # 错误信息
                'K': 20   # 逻辑分析
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # 创建统计信息表
            stats_data = []
            successful_comparisons = sum(1 for r in results if r['status'] == 'success')
            failed_comparisons = len(results) - successful_comparisons
            
            stats_data.append(['总比较次数', len(results)])
            stats_data.append(['成功比较', successful_comparisons])
            stats_data.append(['失败比较', failed_comparisons])
            
            # 逻辑分析统计
            logic_analysis_count = sum(1 for r in results if r.get('logic_analysis'))
            same_person_failures = sum(1 for r in results if r.get('logic_analysis') == '同一个人比对失败')
            different_person_high_similarity = sum(1 for r in results if r.get('logic_analysis') == '不同人相似度高')
            
            stats_data.append(['逻辑分析标识总数', logic_analysis_count])
            stats_data.append(['同一个人比对失败', same_person_failures])
            stats_data.append(['不同人相似度高', different_person_high_similarity])
            
            if successful_comparisons > 0:
                valid_results = [r for r in results if r['status'] == 'success' and r['similarity_score'] is not None]
                if valid_results:
                    max_similarity = max(valid_results, key=lambda x: x['similarity_score'])
                    min_similarity = min(valid_results, key=lambda x: x['similarity_score'])
                    
                    stats_data.append(['最高相似度分数', f"{max_similarity['similarity_score']:.4f}"])
                    stats_data.append(['最高相似度文件对', f"{max_similarity['file1']} vs {max_similarity['file2']}"])
                    stats_data.append(['最低相似度分数', f"{min_similarity['similarity_score']:.4f}"])
                    stats_data.append(['最低相似度文件对', f"{min_similarity['file1']} vs {min_similarity['file2']}"])
            
            # 写入统计信息
            stats_df = pd.DataFrame(stats_data, columns=['统计项', '数值'])
            stats_df.to_excel(writer, sheet_name='统计信息', index=False)
            
            # 调整统计信息表的列宽
            stats_worksheet = writer.sheets['统计信息']
            stats_worksheet.column_dimensions['A'].width = 20
            stats_worksheet.column_dimensions['B'].width = 40
        
        print(f"\nExcel文件已保存: {filename}")
        print(f"包含 {len(results)} 条比对记录")
        
        # 提供使用建议
        print(f"\n使用建议:")
        print(f"1. 打开Excel文件查看详细结果")
        print(f"2. 使用'比对结果'表进行排序和筛选")
        print(f"3. 查看'统计信息'表了解整体情况")
        print(f"4. 关注'逻辑分析'列中的特殊情况")
        print(f"5. 可以根据相似度分数进行进一步分析")
        
    except Exception as e:
        print(f"保存Excel文件失败: {str(e)}")
        print("尝试保存为文本文件...")
        save_results_to_file(results)

def save_results_to_file(results):
    """
    将比对结果保存到文本文件（备用方案）
    
    Args:
        results (list): 比对结果列表
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_similarity_results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("音频文件相似度对比结果\n")
            f.write("="*80 + "\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"比较 {i}:\n")
                f.write(f"  文件1: {result['file1']}\n")
                f.write(f"  文件2: {result['file2']}\n")
                
                if result['status'] == 'success':
                    f.write(f"  相似度分数: {result['similarity_score']:.4f}\n")
                    f.write(f"  相似度百分比: {result['similarity_percentage']:.2f}%\n")
                    f.write(f"  相似度描述: {result['description']}\n")
                else:
                    f.write(f"  状态: 失败\n")
                    f.write(f"  错误信息: {result['error_message']}\n")
                
                # 添加逻辑分析
                if result.get('logic_analysis'):
                    f.write(f"  逻辑分析: {result['logic_analysis']}\n")
                
                f.write("\n")
        
        print(f"\n文本文件已保存: {filename}")
        
    except Exception as e:
        print(f"保存文本文件失败: {str(e)}")

def main():
    """
    主函数
    """
    print("音频相似度分析工具")
    print("=" * 50)
    
    # 检查Excel支持
    if not EXCEL_AVAILABLE:
        print("注意: pandas 未安装，将使用文本格式输出结果")
        print("建议安装: pip install pandas openpyxl")
    
    while True:
        print("\n请选择操作:")
        print("1. 基本使用示例 (使用默认文件)")
        print("2. 自定义路径示例")
        print("3. 批量分析示例")
        print("4. 所有音频文件比对分析 (输出Excel表格)")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            example_basic_usage()
        elif choice == '2':
            example_custom_paths()
        elif choice == '3':
            example_batch_analysis()
        elif choice == '4':
            # 新增：询问目录
            dir_input = input("请输入要分析的目录（直接回车默认files目录）: ").strip()
            if dir_input:
                example_all_files_comparison(dir_input)
            else:
                example_all_files_comparison()
        elif choice == '5':
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 