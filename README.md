# 实时汇率与贵金属价格桌面应用

![示例截图](screenshots/app_screenshot.png)

## 项目简介

这是一个无边框桌面应用程序，实时显示主要货币汇率和贵金属价格。应用程序自动更新数据，支持无边框拖拽、窗口置顶和开机自启等功能。

## 特色功能

- **实时数据更新**: 每60秒自动更新一次货币汇率和贵金属价格
- **贵金属价格**: 显示黄金、白银、铂金、钯金的实时买入卖出价格
- **多种货币支持**: 包含主要货币(美元、欧元、英镑、日元、港币)和其他常用货币的汇率
- **无边框设计**: 现代简洁的无边框界面设计
- **置顶功能**: 可以将窗口固定在屏幕最上层
- **位置锁定**: 锁定窗口位置，防止误移动
- **开机自启**: 支持设置开机自动启动
- **完全免费**: 使用开源API，无需任何费用

## 数据来源

- 贵金属价格数据来源: https://free.xwteam.cn/api/gold/trade
- 货币汇率数据来源: https://api.exchangerate-api.com/v4/latest/CNY

## 安装方法

### 方法一: 直接下载可执行文件

在 [Releases](https://github.com/1351055318/HUILV/releases) 页面下载最新版本的可执行文件，解压后直接运行 `汇率与贵金属价格.exe`。

### 方法二: 从源码运行

1. 克隆仓库
   ```bash
   git clone https://github.com/1351055318/HUILV.git
   cd HUILV
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序
   ```bash
   python main.py
   ```

## 使用说明

- **拖动**: 用鼠标左键拖动窗口可以移动位置
- **刷新**: 点击"刷新"按钮手动更新数据
- **置顶**: 点击"置顶"按钮切换窗口是否置顶显示
- **锁定**: 点击"锁定"按钮锁定窗口位置，防止误拖动
- **右键菜单**: 右键点击窗口可以打开菜单，包含更多选项
  - 锁定/解锁位置
  - 置顶/取消置顶
  - 开机自启/取消自启
  - 最小化
  - 关闭

## 构建可执行文件

如果您想从源码构建可执行文件，可以使用以下命令：

```bash
# 安装 PyInstaller
pip install PyInstaller

# 构建单文件版本
python -m PyInstaller --name="汇率与贵金属价格" --windowed --onefile main.py
```

## 技术栈

- **Python**: 核心编程语言
- **PySide6**: 用于创建GUI界面
- **Requests**: 用于API调用获取实时数据

## 贡献指南

欢迎提交问题和改进建议！请遵循以下步骤：

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 许可证

此项目采用 MIT 许可证 - 详情见 [LICENSE](LICENSE) 文件

## 联系方式

GitHub: [@1351055318](https://github.com/1351055318)

---

*注: 本程序仅供学习和参考使用，数据来源于第三方API，不保证数据的准确性和及时性。* 