import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QDateTimeEdit, QLineEdit, 
                            QCheckBox, QGroupBox, QMessageBox, QSpacerItem,
                            QSizePolicy, QMainWindow, QRadioButton, QSlider,
                            QColorDialog)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import QTimer, QDateTime, Qt, QSettings, QPoint

class CountdownWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("桌面倒计时")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Load settings
        self.settings = QSettings("CountdownApp", "DesktopCountdown")
        self.display_text = self.settings.value("display_text", "目标时间还有: ")
        self.target_time = QDateTime.currentDateTime().addSecs(3600)
        saved_time = self.settings.value("target_time")
        if saved_time:
            self.target_time = QDateTime.fromString(saved_time, Qt.ISODate)
        
        # Theme settings
        self.bg_opacity = self.settings.value("bg_opacity", 200, type=int)
        self.bg_color = self.settings.value("bg_color", "40,40,40", type=str)
        self.text_color = self.settings.value("text_color", "255,255,255", type=str)
        self.font_size = self.settings.value("font_size", 42, type=int)
        self.alignment = self.settings.value("alignment", "center")
        self.auto_wallpaper = self.settings.value("auto_wallpaper", False, type=bool)
        self.auto_start = self.settings.value("auto_start", False, type=bool)
        self.auto_continue = self.settings.value("auto_continue", True, type=bool)
        
        # Initialize UI
        self.init_ui()
        self.center_on_screen()
        
        # Initialize timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        
        # Auto-start if enabled and target time is in future
        if self.auto_continue and self.target_time > QDateTime.currentDateTime():
            self.start_countdown()
    
    def init_ui(self):
        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        
        # Countdown display
        self.countdown_label = QLabel(self.get_display_text("00:00:00"))
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.update_label_style()
        main_layout.addWidget(self.countdown_label)
        
        # Settings button
        self.settings_button = QPushButton("⚙️ 设置")
        self.settings_button.setFixedSize(100, 40)
        self.settings_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                border: none;
                background-color: rgba(60, 60, 60, 150);
                border-radius: 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 150);
            }
        """)
        self.settings_button.clicked.connect(self.show_settings_window)
        
        # Put settings button in bottom right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.settings_button)
        main_layout.addLayout(button_layout)
    
    def get_display_text(self, time_str):
        return f"{self.display_text}{time_str}"
    
    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        window_geometry = self.frameGeometry()
        
        if self.alignment == "center":
            window_geometry.moveCenter(screen_geometry.center())
        elif self.alignment == "bottom_right":
            window_geometry.moveBottomRight(screen_geometry.bottomRight() - QPoint(20, 20))
        elif self.alignment == "top_right":
            window_geometry.moveTopRight(screen_geometry.topRight() + QPoint(-20, 20))
            
        self.move(window_geometry.topLeft())
    
    def show_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
    
    def start_countdown(self):
        self.timer.start(1000)
        self.update_countdown()
    
    def update_label_style(self):
        r, g, b = map(int, self.bg_color.split(','))
        tr, tg, tb = map(int, self.text_color.split(','))
        
        self.countdown_label.setStyleSheet(f"""
            QLabel {{
                font-size: {self.font_size}px;
                font-weight: bold;
                color: rgba({tr}, {tg}, {tb}, 255);
                background-color: rgba({r}, {g}, {b}, {self.bg_opacity});
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        self.adjust_window_size()

    def adjust_window_size(self):
        # Calculate required size based on text
        self.countdown_label.adjustSize()
        label_size = self.countdown_label.sizeHint()
        
        # Calculate window size (width + margins, fixed height)
        width = min(max(label_size.width() + 50, 300), 800)  # Min 300, max 800
        height = 200  # Fixed height
        
        # Adjust window and label size
        self.resize(width, height)
        self.countdown_label.setFixedWidth(width - 50)
        
        # Re-center window
        self.center_on_screen()

    def update_countdown(self):
        now = QDateTime.currentDateTime()
        seconds_remaining = now.secsTo(self.target_time)
        
        if seconds_remaining <= 0:
            self.countdown_label.setText(self.get_display_text("时间到！"))
            self.timer.stop()
        elif seconds_remaining > 86400:
            days = seconds_remaining // 86400
            self.countdown_label.setText(self.get_display_text(f"{days}天"))
        else:
            hours = seconds_remaining // 3600
            minutes = (seconds_remaining % 3600) // 60
            seconds = seconds_remaining % 60
            self.countdown_label.setText(self.get_display_text(
                f"{hours:02d}:{minutes:02d}:{seconds:02d}"))
        
        # Update window size
        self.adjust_window_size()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("倒计时设置")
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(500, 500)
        
        # Load settings
        self.settings = QSettings("CountdownApp", "DesktopCountdown")
        self.load_settings()
        
        # Initialize UI
        self.init_ui()
        self.center_on_screen()
    
    def load_settings(self):
        self.display_text = self.settings.value("display_text", "目标时间还有: ")
        self.target_time = self.settings.value("target_time", QDateTime.currentDateTime().addSecs(3600))
        if isinstance(self.target_time, str):
            self.target_time = QDateTime.fromString(self.target_time, Qt.ISODate)
        self.auto_start = self.settings.value("auto_start", False, type=bool)
        self.auto_continue = self.settings.value("auto_continue", True, type=bool)
        self.bg_opacity = self.settings.value("bg_opacity", 200, type=int)
        self.bg_color = self.settings.value("bg_color", "40,40,40", type=str)
        self.text_color = self.settings.value("text_color", "255,255,255", type=str)
        self.font_size = self.settings.value("font_size", 42, type=int)
        self.alignment = self.settings.value("alignment", "center")
        self.auto_wallpaper = self.settings.value("auto_wallpaper", False, type=bool)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Display text
        text_group = QHBoxLayout()
        text_label = QLabel("显示文字：")
        text_label.setStyleSheet("font-size: 16px;")
        self.text_input = QLineEdit(self.display_text)
        self.text_input.setStyleSheet("font-size: 16px; padding: 8px;")
        text_group.addWidget(text_label)
        text_group.addWidget(self.text_input)
        main_layout.addLayout(text_group)
        
        # Target time
        datetime_group = QHBoxLayout()
        datetime_label = QLabel("目标时间：")
        datetime_label.setStyleSheet("font-size: 16px;")
        self.datetime_edit = QDateTimeEdit(self.target_time)
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setStyleSheet("font-size: 16px; padding: 8px;")
        datetime_group.addWidget(datetime_label)
        datetime_group.addWidget(self.datetime_edit)
        main_layout.addLayout(datetime_group)
        
        # Theme settings
        theme_group = QGroupBox("主题设置")
        theme_layout = QVBoxLayout()
        
        # Background color
        color_layout = QHBoxLayout()
        color_label = QLabel("背景颜色(R,G,B):")
        self.color_input = QLineEdit(self.bg_color)
        color_picker_btn = QPushButton("选择")
        color_picker_btn.clicked.connect(self.pick_bg_color)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_input)
        color_layout.addWidget(color_picker_btn)
        theme_layout.addLayout(color_layout)
        
        # Text color
        text_color_layout = QHBoxLayout()
        text_color_label = QLabel("文字颜色(R,G,B):")
        self.text_color_input = QLineEdit(self.text_color)
        text_color_picker_btn = QPushButton("选择")
        text_color_picker_btn.clicked.connect(self.pick_text_color)
        text_color_layout.addWidget(text_color_label)
        text_color_layout.addWidget(self.text_color_input)
        text_color_layout.addWidget(text_color_picker_btn)
        theme_layout.addLayout(text_color_layout)
        
        # Font size
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel(f"字体大小({self.font_size}px):")
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setRange(12, 72)
        self.font_size_slider.setValue(self.font_size)
        self.font_size_slider.valueChanged.connect(
            lambda v: font_size_label.setText(f"字体大小({v}px):"))
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_slider)
        theme_layout.addLayout(font_size_layout)
        
        # Opacity slider
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel(f"透明度({self.bg_opacity}):")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 255)
        self.opacity_slider.setValue(self.bg_opacity)
        self.opacity_slider.valueChanged.connect(
            lambda v: opacity_label.setText(f"透明度({v}):"))
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        theme_layout.addLayout(opacity_layout)
        
        # Theme presets
        theme_preset_layout = QHBoxLayout()
        dark_btn = QPushButton("深色主题")
        light_btn = QPushButton("浅色主题")
        blue_btn = QPushButton("蓝色主题")
        
        dark_btn.clicked.connect(lambda: self.set_theme_preset("40,40,40", "255,255,255", 42, 200))
        light_btn.clicked.connect(lambda: self.set_theme_preset("220,220,220", "0,0,0", 42, 180))
        blue_btn.clicked.connect(lambda: self.set_theme_preset("30,80,150", "255,255,255", 42, 180))
        
        theme_preset_layout.addWidget(dark_btn)
        theme_preset_layout.addWidget(light_btn)
        theme_preset_layout.addWidget(blue_btn)
        theme_layout.addLayout(theme_preset_layout)
        
        theme_group.setLayout(theme_layout)
        main_layout.addWidget(theme_group)
        
        # Window position
        pos_group = QGroupBox("窗口位置")
        pos_layout = QVBoxLayout()
        
        self.center_radio = QRadioButton("居中对齐")
        self.bottom_right_radio = QRadioButton("右下对齐")
        self.top_right_radio = QRadioButton("右上对齐")
        
        if self.alignment == "center":
            self.center_radio.setChecked(True)
        elif self.alignment == "bottom_right":
            self.bottom_right_radio.setChecked(True)
        else:
            self.top_right_radio.setChecked(True)
            
        pos_layout.addWidget(self.center_radio)
        pos_layout.addWidget(self.bottom_right_radio)
        pos_layout.addWidget(self.top_right_radio)
        pos_group.setLayout(pos_layout)
        main_layout.addWidget(pos_group)
        
        # Auto settings
        auto_group = QGroupBox("自动设置")
        auto_layout = QVBoxLayout()
        
        self.auto_start_check = QCheckBox("开机自启动")
        self.auto_start_check.setChecked(self.auto_start)
        self.auto_continue_check = QCheckBox("自动继续未完成计时")
        self.auto_continue_check.setChecked(self.auto_continue)
        self.auto_wallpaper_check = QCheckBox("自动适应壁纸颜色")
        self.auto_wallpaper_check.setChecked(self.auto_wallpaper)
        
        auto_layout.addWidget(self.auto_start_check)
        auto_layout.addWidget(self.auto_continue_check)
        auto_layout.addWidget(self.auto_wallpaper_check)
        auto_group.setLayout(auto_layout)
        main_layout.addWidget(auto_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存设置")
        self.save_button.setStyleSheet("font-size: 16px; padding: 8px;")
        self.save_button.clicked.connect(self.save_settings)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet("font-size: 16px; padding: 8px;")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Window style
        self.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei";
            }
            QPushButton {
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                min-width: 80px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QDateTimeEdit {
                padding: 10px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
                min-width: 200px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QGroupBox {
                border: 1px solid gray;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
    
    def pick_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setText(f"{color.red()},{color.green()},{color.blue()}")
    
    def pick_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color_input.setText(f"{color.red()},{color.green()},{color.blue()}")
    
    def set_theme_preset(self, bg_color, text_color, font_size, opacity):
        self.color_input.setText(bg_color)
        self.text_color_input.setText(text_color)
        self.font_size_slider.setValue(font_size)
        self.opacity_slider.setValue(opacity)
    
    def save_settings(self):
        # Validate inputs
        try:
            bg_color = self.color_input.text()
            parts = bg_color.split(',')
            if len(parts) != 3 or not all(0 <= int(x) <= 255 for x in parts):
                raise ValueError("背景颜色格式应为R,G,B (0-255)")
            
            text_color = self.text_color_input.text()
            parts = text_color.split(',')
            if len(parts) != 3 or not all(0 <= int(x) <= 255 for x in parts):
                raise ValueError("文字颜色格式应为R,G,B (0-255)")
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
            return
        
        # Save settings
        self.display_text = self.text_input.text()
        self.target_time = self.datetime_edit.dateTime()
        self.auto_start = self.auto_start_check.isChecked()
        self.auto_continue = self.auto_continue_check.isChecked()
        self.auto_wallpaper = self.auto_wallpaper_check.isChecked()
        self.bg_color = self.color_input.text()
        self.text_color = self.text_color_input.text()
        self.font_size = self.font_size_slider.value()
        self.bg_opacity = self.opacity_slider.value()
        
        if self.center_radio.isChecked():
            self.alignment = "center"
        elif self.bottom_right_radio.isChecked():
            self.alignment = "bottom_right"
        else:
            self.alignment = "top_right"
        
        self.settings.setValue("display_text", self.display_text)
        self.settings.setValue("target_time", self.target_time.toString(Qt.ISODate))
        self.settings.setValue("auto_start", self.auto_start)
        self.settings.setValue("auto_continue", self.auto_continue)
        self.settings.setValue("auto_wallpaper", self.auto_wallpaper)
        self.settings.setValue("bg_color", self.bg_color)
        self.settings.setValue("text_color", self.text_color)
        self.settings.setValue("font_size", self.font_size)
        self.settings.setValue("bg_opacity", self.bg_opacity)
        self.settings.setValue("alignment", self.alignment)
        
        # Update parent window
        self.parent.display_text = self.display_text
        self.parent.target_time = self.target_time
        self.parent.bg_color = self.bg_color
        self.parent.text_color = self.text_color
        self.parent.font_size = self.font_size
        self.parent.bg_opacity = self.bg_opacity
        self.parent.alignment = self.alignment
        self.parent.auto_wallpaper = self.auto_wallpaper
        
        self.parent.update_label_style()
        
        if self.parent.timer.isActive():
            self.parent.update_countdown()
        else:
            self.parent.countdown_label.setText(self.parent.get_display_text("00:00:00"))
        
        # Set auto-start
        self.set_auto_start(self.auto_start)
        
        QMessageBox.information(self, "提示", "设置已保存！")
        self.close()
    
    def set_auto_start(self, enable):
        if sys.platform == "win32":
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE) as reg_key:
                    if enable:
                        winreg.SetValueEx(reg_key, "DesktopCountdown", 0, winreg.REG_SZ, 
                                        f'"{sys.executable}" "{os.path.abspath(__file__)}"')
                    else:
                        try:
                            winreg.DeleteValue(reg_key, "DesktopCountdown")
                        except WindowsError:
                            pass
            except WindowsError:
                QMessageBox.warning(self, "警告", "无法设置开机自启动！")
    
    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application icon
    app_icon = QIcon()
    icon_paths = [
        "logo.ico",  # Current directory
        os.path.join(os.path.dirname(sys.executable), "logo.ico"),  # Executable directory
        os.path.join(os.path.dirname(__file__), "logo.ico")  # Script directory
    ]
    
    for path in icon_paths:
        if os.path.exists(path):
            app_icon.addFile(path)
            break
    
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)
    
    window = CountdownWindow()
    window.show()
    sys.exit(app.exec_())