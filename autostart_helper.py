"""
提供更可靠的开机自启动功能的助手程序
这个文件被主程序调用，处理自启动逻辑
"""

import os
import sys
import winreg
import ctypes

def is_admin():
    """检查程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_app_path():
    """获取应用程序路径"""
    if getattr(sys, 'frozen', False):
        # 打包为exe后的路径
        return sys.executable
    else:
        # 开发环境路径
        return os.path.abspath(sys.argv[0])

def check_auto_start():
    """检查是否已设置为开机自启动"""
    app_path = get_app_path()
    app_name = "CurrencyApp"
    try:
        # 尝试打开注册表
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )
        try:
            # 检查是否已经存在
            value, _ = winreg.QueryValueEx(key, app_name)
            return value == f'"{app_path}"'
        except FileNotFoundError:
            return False
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        print(f"检查自启动设置时出错: {e}")
        return False

def set_auto_start(enable=True):
    """设置或取消开机自启动"""
    app_path = get_app_path()
    app_name = "CurrencyApp"
    
    # 尝试使用普通权限设置
    try:
        # 打开注册表
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE | winreg.KEY_READ
        )
        
        if enable:
            # 添加到自启动
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{app_path}"')
        else:
            # 从自启动中移除
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
                
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"设置自启动时出错: {e}")
        
        # 如果失败并且不是管理员，可以尝试请求管理员权限
        if not is_admin():
            return False
            
    return False 