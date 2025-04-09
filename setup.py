import sys
from cx_Freeze import setup, Executable

# 依赖项
build_exe_options = {
    "packages": ["os", "sys", "PySide6", "requests", "datetime", "time", "winreg"],
    "excludes": ["tkinter", "matplotlib", "numpy"],
    "include_files": [],
    "optimize": 2,
}

# 基本信息
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 使用Windows GUI程序

executables = [
    Executable(
        "main.py",  # 主文件
        base=base,
        target_name="汇率与贵金属价格.exe",  # 程序名称
        icon=None,  # 可以添加图标
        shortcut_name="汇率与贵金属价格",
        shortcut_dir="DesktopFolder",
    )
]

setup(
    name="汇率与贵金属价格",
    version="1.0.0",
    description="实时显示贵金属价格和主要货币汇率",
    author="XWTeam",
    options={"build_exe": build_exe_options},
    executables=executables,
) 