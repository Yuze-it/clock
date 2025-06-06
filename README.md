# Desktop Countdown 桌面倒计时

A customizable desktop countdown timer application built with PyQt5.  
使用 PyQt5 构建的可定制桌面倒计时应用。

## Features 功能特点

- 🕒 Custom countdown to any target date/time  
  自定义目标日期/时间的倒计时
- 🎨 Fully customizable appearance (colors, font size, opacity)  
  完全可定制的外观（颜色、字体大小、透明度）
- 🖥️ Multiple window position options (center, top right, bottom right)  
  多种窗口位置选项（居中、右上、右下）
- ⚙️ Settings saved between sessions  
  设置自动保存
- 🚀 Optional auto-start with system  
  可选开机自启动
- 🕶️ Transparent background  
  透明背景
- 🖱️ Draggable window  
  可拖动窗口

## Installation 安装

### Prerequisites 先决条件
- Python 3.6+
- PyQt5

### Steps 步骤
1. Clone this repository  
   克隆本仓库
   ```bash
   git clone https://github.com/Yuze-it/clock.git
   cd clock
   ```

2. Install dependencies  
   安装依赖
   ```bash
   pip install PyQt5
   ```

3. Run the application  
   运行应用
   ```bash
   python desktop_countdown.py
   ```

For Windows users, you can also download the pre-built executable from Releases.  
Windows用户也可以从Releases下载预构建的可执行文件。

## Usage 使用方法

1. **Set Target Time**  
   **设置目标时间**
   - Click the settings button (⚙️)  
     点击设置按钮(⚙️)
   - Choose your target date/time  
     选择目标日期/时间

2. **Customize Appearance**  
   **自定义外观**
   - Change colors, font size and opacity  
     更改颜色、字体大小和透明度
   - Choose window position  
     选择窗口位置
   - Apply theme presets (dark/light/blue)  
     应用主题预设（深色/浅色/蓝色）

3. **Start Countdown**  
   **开始倒计时**
   - The countdown will begin automatically  
     倒计时将自动开始
   - Drag the window to reposition  
     拖动窗口可重新定位

## Settings 设置选项

- **General 常规**
  - Display text 显示文字
  - Target time 目标时间
  - Auto-start with system 开机自启动
  - Auto-continue unfinished countdown 自动继续未完成倒计时

- **Appearance 外观**
  - Background color 背景颜色
  - Text color 文字颜色
  - Font size 字体大小
  - Opacity 透明度
  - Window position 窗口位置

## Build Executable 构建可执行文件

To build a standalone executable using PyInstaller:  
使用PyInstaller构建独立可执行文件：

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=logo.ico desktop_countdown.py
```

## Contributing 贡献

Contributions are welcome! Please open an issue or submit a pull request.  
欢迎贡献！请提交issue或pull request。

## License 许可证

MIT License  
MIT 许可证

---

**Note**: The application icon (logo.ico) should be placed in the same directory as the script.  
**注意**：应用图标(logo.ico)应放在与脚本相同的目录中。

```
Downloading directly from GitHub may not run properly. Please visit https://clock-yuze.netlify.app to view and download.
直接在github下载可能无法直接运行，请在 https://clock-yuze.netlify.app 查看并下载
