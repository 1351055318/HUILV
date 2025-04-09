"""
使用 PyInstaller 打包应用程序
运行方式：python pyinstaller_build.py
"""

import os
import sys
import PyInstaller.__main__

print("开始打包应用程序...")

# 定义打包参数
PyInstaller.__main__.run([
    "--name=汇率与贵金属价格",
    "--windowed",  # 使用窗口模式（无控制台）
    "--noconfirm",  # 不询问确认
    "--clean",  # 清理临时文件
    "--onedir",  # 创建单目录包（如果需要单文件可改为 --onefile）
    "--add-data=requirements.txt;.",  # 添加数据文件
    # 以下是依赖的模块和库
    "--hidden-import=winreg",
    "--hidden-import=time",
    "--hidden-import=datetime",
    "--hidden-import=requests",
    "--hidden-import=PySide6",
    "main.py"  # 主程序文件
])

print("\n打包完成！应用程序在 dist/汇率与贵金属价格 目录中。") 