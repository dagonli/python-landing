# 音频处理工具集

这是一个完整的音频处理工具集，包含音频相似度分析和音频格式转换功能。

## 功能特性

### 音频相似度分析
- 支持 WAV 格式音频文件
- 使用 resemblyzer 进行音频特征提取
- 计算余弦相似度来判断音频相似性
- 提供详细的相似度分数和描述
- 支持批量分析和自定义路径
- 完整的错误处理和日志记录
- **Excel格式结果输出** - 支持排序、筛选和数据分析

### 音频格式转换
- 支持多种音频格式转换为 WAV 格式
- 支持 MP3, FLAC, AAC, OGG, M4A, WMA 等常见格式
- 支持视频文件中的音频提取
- 可自定义输出采样率和声道数
- 支持批量转换
- 多种转换方法（librosa, pydub, ffmpeg）

## 安装依赖

### 方法1: 使用安装脚本（推荐）
```bash
python install_dependencies.py
```

### 方法2: 手动安装
```bash
pip install -r requirements.txt
```

### 方法3: 单独安装
```bash
pip install resemblyzer numpy librosa torch torchaudio scipy pydub soundfile pandas openpyxl
```

## 文件说明

- `audio_similarity.py` - 音频相似度分析类
- `audio_converter.py` - 音频格式转换类
- `example_usage.py` - 音频相似度分析使用示例（包含Excel输出）
- `converter_example.py` - 音频转换使用示例
- `test_comparison.py` - 音频比对功能测试脚本
- `install_dependencies.py` - 依赖包安装脚本
- `requirements.txt` - 依赖包列表
- `client_1.wav` - 示例音频文件1
- `client_2.wav` - 示例音频文件2

## 使用方法

### 1. 音频相似度分析

#### 基本使用
```python
from audio_similarity import AudioSimilarityAnalyzer

# 创建分析器实例
analyzer = AudioSimilarityAnalyzer()

# 比较两个音频文件
result = analyzer.compare_audio_files("audio1.wav", "audio2.wav")

# 查看结果
if result['status'] == 'success':
    print(f"相似度: {result['similarity_score']:.4f}")
    print(f"相似度百分比: {result['similarity_percentage']:.2f}%")
    print(f"描述: {analyzer.get_similarity_description(result['similarity_score'])}")
```

#### 运行示例程序
```bash
python example_usage.py
```

#### 批量比对所有音频文件
```bash
python test_comparison.py
```

### 2. 音频格式转换

#### 基本使用
```python
from audio_converter import AudioConverter

# 创建转换器实例
converter = AudioConverter(output_sample_rate=16000, output_channels=1)

# 转换单个文件
result = converter.convert_to_wav("input.mp3")

# 查看结果
if result['status'] == 'success':
    print(f"转换成功: {result['output_path']}")
    print(f"使用方法: {result['used_method']}")
```

#### 批量转换
```python
# 批量转换文件
files = ["audio1.mp3", "audio2.flac", "audio3.aac"]
result = converter.batch_convert(files, output_dir="converted/")

print(f"成功转换: {result['successful_conversions']}/{result['total_files']}")
```

#### 运行转换示例程序
```bash
python converter_example.py
```

## Excel输出功能

### 功能特点
- **自动生成Excel文件** - 包含时间戳的文件名
- **两个工作表** - "比对结果"和"统计信息"
- **格式化表格** - 自动调整列宽，便于查看
- **完整数据** - 包含文件路径、相似度分数、描述等
- **统计信息** - 最高/最低相似度、成功/失败统计

### Excel文件结构

#### "比对结果"工作表
| 列名 | 说明 |
|------|------|
| 序号 | 比对序号 |
| 文件1 | 第一个音频文件名 |
| 文件2 | 第二个音频文件名 |
| 文件1路径 | 第一个音频文件完整路径 |
| 文件2路径 | 第二个音频文件完整路径 |
| 相似度分数 | 0-1之间的相似度分数 |
| 相似度百分比 | 百分比形式的相似度 |
| 相似度描述 | 相似度的文字描述 |
| 状态 | 成功/失败 |
| 错误信息 | 失败时的错误信息 |

#### "统计信息"工作表
| 统计项 | 数值 |
|--------|------|
| 总比较次数 | 总比对次数 |
| 成功比较 | 成功完成的比对次数 |
| 失败比较 | 失败的比对次数 |
| 最高相似度分数 | 最高相似度分数 |
| 最高相似度文件对 | 最高相似度的文件对 |
| 最低相似度分数 | 最低相似度分数 |
| 最低相似度文件对 | 最低相似度的文件对 |

### 使用建议
1. **排序分析** - 按相似度分数排序，找出最相似的文件对
2. **筛选功能** - 筛选特定相似度范围的结果
3. **数据透视** - 使用Excel的数据透视表功能进行深入分析
4. **图表制作** - 基于相似度数据制作图表

## API 文档

### AudioSimilarityAnalyzer 类

#### 初始化
```python
analyzer = AudioSimilarityAnalyzer(model_path=None)
```

#### 主要方法

1. **compare_audio_files(audio_path1, audio_path2)**
   - 比较两个音频文件的相似度
   - 参数: `audio_path1, audio_path2` (str) - 音频文件路径
   - 返回: 包含相似度信息的字典

2. **get_similarity_description(similarity_score)**
   - 根据相似度分数返回描述性文本
   - 参数: `similarity_score` (float) - 相似度分数
   - 返回: 相似度描述字符串

### AudioConverter 类

#### 初始化
```python
converter = AudioConverter(output_sample_rate=16000, output_channels=1)
```

#### 主要方法

1. **convert_to_wav(input_path, output_path=None)**
   - 将音频文件转换为 WAV 格式
   - 参数: `input_path` (str) - 输入文件路径, `output_path` (str, optional) - 输出文件路径
   - 返回: 转换结果字典

2. **batch_convert(input_files, output_dir=None)**
   - 批量转换音频文件
   - 参数: `input_files` (list) - 输入文件列表, `output_dir` (str, optional) - 输出目录
   - 返回: 批量转换结果字典

3. **get_file_info(file_path)**
   - 获取音频文件信息
   - 参数: `file_path` (str) - 文件路径
   - 返回: 文件信息字典

4. **is_supported_format(file_path)**
   - 检查文件格式是否支持
   - 参数: `file_path` (str) - 文件路径
   - 返回: 是否支持该格式

## 支持的音频格式

### 音频相似度分析
- WAV 格式（其他格式会自动转换为WAV）

### 音频格式转换
- **音频格式**: MP3, FLAC, AAC, OGG, WMA, M4A, OPUS, WEBM, 3GP, AMR, AU, AIFF, WV, APE, RA, RM, ASF
- **视频格式**: AVI, MKV, MP4, MOV (提取音频)

## 相似度评分说明

- **0.9-1.0**: 极高相似度 - 很可能是同一个人的声音
- **0.8-0.9**: 高相似度 - 可能是同一个人的声音
- **0.7-0.8**: 中等相似度 - 可能是相似的声音特征
- **0.5-0.7**: 低相似度 - 声音特征有一定差异
- **0.0-0.5**: 极低相似度 - 声音特征差异很大

## 转换方法

音频转换器支持多种转换方法，按优先级顺序：

1. **librosa** - 基于 librosa 库的转换
2. **pydub** - 基于 pydub 库的转换
3. **ffmpeg** - 基于系统 ffmpeg 的转换（如果已安装）

## 注意事项

### 音频相似度分析
1. 支持多种音频格式，非WAV格式会自动转换
2. 音频文件应该包含清晰的人声内容
3. 音频质量会影响相似度分析的准确性
4. 首次运行时会下载 resemblyzer 的预训练模型
5. Excel输出需要安装 pandas 和 openpyxl

### 音频格式转换
1. 支持多种音频和视频格式
2. 可自定义输出采样率和声道数
3. 转换质量取决于输入文件质量和选择的转换方法
4. 某些格式可能需要额外的编解码器支持

## 错误处理

程序包含完整的错误处理机制：
- 文件不存在检查
- 文件格式验证
- 音频处理异常捕获
- 详细的错误信息输出
- 转换失败时的回退机制
- Excel输出失败时自动回退到文本格式

## 示例输出

### 控制台输出
```
========================================================================================================================
音频文件相似度对比结果表
========================================================================================================================
序号 文件1                文件2                相似度分数    相似度百分比  相似度描述                    状态    
------------------------------------------------------------------------------------------------------------------------
1    李豫1.wav            李豫2.wav            0.8234       82.34%      高相似度 - 可能是同一个人的声音  成功    
2    李豫1.wav            李豫3.wav            0.7567       75.67%      中等相似度 - 可能是相似的声音特征  成功    
...
------------------------------------------------------------------------------------------------------------------------
统计信息:
  总比较次数: 15
  成功比较: 15
  失败比较: 0
  最高相似度: 0.8234 (李豫1.wav vs 李豫2.wav)
  最低相似度: 0.2345 (胡亚军1.wav vs 张璐1.wav)
========================================================================================================================

Excel文件已保存: audio_similarity_results_20241201_143022.xlsx
包含 15 条比对记录

使用建议:
1. 打开Excel文件查看详细结果
2. 使用'比对结果'表进行排序和筛选
3. 查看'统计信息'表了解整体情况
4. 可以根据相似度分数进行进一步分析
```

### Excel文件
- 文件名格式: `audio_similarity_results_YYYYMMDD_HHMMSS.xlsx`
- 包含两个工作表: "比对结果" 和 "统计信息"
- 自动格式化，便于查看和分析

## 技术原理

### 音频相似度分析
该工具使用 resemblyzer 库进行音频特征提取：
1. 使用预训练的神经网络模型提取音频的嵌入向量
2. 通过余弦相似度计算两个音频向量的相似性
3. 相似度分数范围在 0-1 之间，分数越高表示越相似

### 音频格式转换
该工具使用多种方法进行音频转换：
1. librosa - 专业的音频处理库
2. pydub - 简单易用的音频处理库
3. ffmpeg - 强大的多媒体处理工具

### Excel输出
该工具使用 pandas 和 openpyxl 进行Excel文件生成：
1. pandas - 数据处理和DataFrame操作
2. openpyxl - Excel文件格式支持
3. 自动格式化和列宽调整

## 许可证

本项目基于 MIT 许可证开源。 