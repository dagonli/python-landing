#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖包安装脚本
帮助用户安装音频处理和Excel输出所需的依赖包
"""

import subprocess
import sys
import os

def install_package(package):
    """
    安装指定的包
    
    Args:
        package (str): 包名
        
    Returns:
        bool: 安装是否成功
    """
    try:
        print(f"正在安装 {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {str(e)}")
        return False

def check_package(package):
    """
    检查包是否已安装
    
    Args:
        package (str): 包名
        
    Returns:
        bool: 是否已安装
    """
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    """
    主函数
    """
    print("音频处理工具依赖包安装脚本")
    print("=" * 50)
    
    # 需要安装的包列表
    packages = [
        "resemblyzer>=0.1.1",
        "numpy>=1.19.0",
        "librosa>=0.8.0",
        "torch>=1.7.0",
        "torchaudio>=0.7.0",
        "scipy>=1.5.0",
        "pydub>=0.25.1",
        "soundfile>=0.10.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0"
    ]
    
    # 检查已安装的包
    print("检查已安装的包...")
    installed_packages = []
    missing_packages = []
    
    for package in packages:
        package_name = package.split('>=')[0].split('==')[0]
        if check_package(package_name):
            print(f"✓ {package_name} 已安装")
            installed_packages.append(package)
        else:
            print(f"✗ {package_name} 未安装")
            missing_packages.append(package)
    
    print(f"\n已安装: {len(installed_packages)}/{len(packages)} 个包")
    
    if not missing_packages:
        print("所有依赖包都已安装完成！")
        return
    
    # 询问是否安装缺失的包
    print(f"\n发现 {len(missing_packages)} 个缺失的包:")
    for package in missing_packages:
        print(f"  - {package}")
    
    choice = input("\n是否安装这些缺失的包？(y/n): ").strip().lower()
    
    if choice not in ['y', 'yes', '是']:
        print("取消安装")
        return
    
    # 安装缺失的包
    print(f"\n开始安装缺失的包...")
    success_count = 0
    
    for package in missing_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{len(missing_packages)} 个包安装成功")
    
    if success_count == len(missing_packages):
        print("所有依赖包安装完成！现在可以使用音频处理工具了。")
    else:
        print("部分包安装失败，请手动安装或检查网络连接。")
        print("可以尝试运行: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 