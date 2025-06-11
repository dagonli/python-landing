from pathlib import Path
import pandas as pd


# 读取当前目录下的 Excel 文件
df = pd.read_excel("demo.xlsx")  # 注意：不是 .excel，正确后缀是 .xlsx 或 .xls

# 提取 C 列（按列号：C 列是第三列，索引为 2）
col_c = df.iloc[:, 2]

# 去除空值并去重
unique_values = col_c.dropna().unique()

# 打印结果
print("C列去重后的条目如下：")
for item in unique_values:
    print(item)
