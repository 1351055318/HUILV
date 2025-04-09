from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QMenu, QSystemTrayIcon,
                           QScrollArea, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint
from PySide6.QtGui import QMouseEvent, QFont, QAction, QColor
from data_fetcher import DataFetcher
import os
import sys
import autostart_helper

class CurrencyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.data_fetcher = DataFetcher()
        self.is_top_most = True
        self.is_position_locked = False
        self.is_auto_start = autostart_helper.check_auto_start()
        self.settings = QSettings("XWTeam", "CurrencyApp")
        self.initUI()
        
        # 用于窗口拖动
        self.oldPos = None
        
        # 设置定时器每60秒更新一次
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rates)
        self.timer.start(60000)  # 60000毫秒 = 1分钟
        
        # 恢复上次的窗口位置
        self.loadSettings()
        
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 240);
                border-radius: 10px;
            }
            QPushButton#actionBtn {
                background-color: rgba(60, 60, 60, 200);
                color: white;
                border: 1px solid #666666;
                border-radius: 3px;
                padding: 3px;
                min-width: 46px;
                font-size: 12px;
            }
            QPushButton#actionBtn:hover {
                background-color: rgba(80, 80, 80, 200);
            }
            QPushButton#actionBtn:checked {
                background-color: rgba(80, 120, 80, 200);
                border-color: #88AA88;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar {
                background-color: transparent;
                width: 0px;
                height: 0px;
            }
            QLabel#sectionTitle {
                color: #AAAAAA;
                font-size: 12px;
                font-weight: bold;
                padding-top: 5px;
                padding-bottom: 3px;
                border-bottom: 1px solid #444444;
            }
            QMenu {
                background-color: rgba(40, 40, 40, 240);
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QMenu::item {
                padding: 5px 18px 5px 18px;
            }
            QMenu::item:selected {
                background-color: rgba(80, 80, 80, 200);
            }
            QWidget#titleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 rgba(35, 35, 35, 240), 
                                      stop:1 rgba(40, 40, 40, 240));
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid #444444;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 5, 10, 5)
        title_layout.setSpacing(0)  # 减少内部间距
        
        title = QLabel('贵金属及汇率价格')
        title.setStyleSheet('color: white; font-size: 14px; font-weight: bold;')
        
        # 按钮容器
        buttons_widget = QWidget()
        buttons_widget.setFixedWidth(170)  # 固定按钮容器宽度
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)  # 增加按钮间距
        
        # 添加刷新按钮
        refresh_btn = QPushButton('刷新')
        refresh_btn.setObjectName("actionBtn")
        refresh_btn.setFixedWidth(46)
        refresh_btn.clicked.connect(lambda: self.update_rates(True))
        
        # 添加置顶按钮
        self.top_most_btn = QPushButton('置顶')
        self.top_most_btn.setObjectName("actionBtn")
        self.top_most_btn.setFixedWidth(46)
        self.top_most_btn.setCheckable(True)
        self.top_most_btn.setChecked(True)
        self.top_most_btn.clicked.connect(self.toggle_top_most)
        
        # 添加锁定位置按钮
        self.lock_pos_btn = QPushButton('锁定')
        self.lock_pos_btn.setObjectName("actionBtn")
        self.lock_pos_btn.setFixedWidth(46)
        self.lock_pos_btn.setCheckable(True)
        self.lock_pos_btn.setChecked(False)
        self.lock_pos_btn.clicked.connect(self.toggle_position_lock)
        
        buttons_layout.addWidget(self.lock_pos_btn)
        buttons_layout.addWidget(self.top_most_btn)
        buttons_layout.addWidget(refresh_btn)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(buttons_widget)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 设置滚动区域样式，隐藏滚动条但保留滚动功能
        scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { width: 0px; }
            QScrollBar:horizontal { height: 0px; }
        """)
        
        # 创建内容部件
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(2)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标签并设置样式
        def create_price_label():
            label = QLabel()
            label.setStyleSheet('color: white; font-size: 13px;')
            label.setAlignment(Qt.AlignLeft)
            label.setContentsMargins(15, 2, 15, 2)
            return label
        
        # 创建贵金属标题
        metals_title = QLabel("贵金属")
        metals_title.setObjectName("sectionTitle")
        metals_title.setAlignment(Qt.AlignLeft)
        metals_title.setContentsMargins(10, 5, 10, 5)
        content_layout.addWidget(metals_title)
        
        # 贵金属价格显示区域
        self.gold_label = create_price_label()
        self.silver_label = create_price_label()
        self.platinum_label = create_price_label()
        self.palladium_label = create_price_label()
        
        content_layout.addWidget(self.gold_label)
        content_layout.addWidget(self.silver_label)
        content_layout.addWidget(self.platinum_label)
        content_layout.addWidget(self.palladium_label)
        
        # 添加主要货币标题
        major_forex_title = QLabel("主要货币")
        major_forex_title.setObjectName("sectionTitle")
        major_forex_title.setAlignment(Qt.AlignLeft)
        major_forex_title.setContentsMargins(10, 10, 10, 5)
        content_layout.addWidget(major_forex_title)
        
        # 主要货币汇率显示区域
        self.usd_label = create_price_label()
        self.eur_label = create_price_label()
        self.gbp_label = create_price_label()
        self.jpy_label = create_price_label()
        self.hkd_label = create_price_label()
        
        content_layout.addWidget(self.usd_label)
        content_layout.addWidget(self.eur_label)
        content_layout.addWidget(self.gbp_label)
        content_layout.addWidget(self.jpy_label)
        content_layout.addWidget(self.hkd_label)
        
        # 添加其他货币标题
        other_forex_title = QLabel("其他货币")
        other_forex_title.setObjectName("sectionTitle")
        other_forex_title.setAlignment(Qt.AlignLeft)
        other_forex_title.setContentsMargins(10, 10, 10, 5)
        content_layout.addWidget(other_forex_title)
        
        # 其他货币汇率显示区域
        self.cad_label = create_price_label()
        self.aud_label = create_price_label()
        self.chf_label = create_price_label()
        self.sgd_label = create_price_label()
        self.krw_label = create_price_label()
        self.thb_label = create_price_label()
        self.rub_label = create_price_label()
        self.myr_label = create_price_label()
        self.nzd_label = create_price_label()
        
        content_layout.addWidget(self.cad_label)
        content_layout.addWidget(self.aud_label)
        content_layout.addWidget(self.chf_label)
        content_layout.addWidget(self.sgd_label)
        content_layout.addWidget(self.krw_label)
        content_layout.addWidget(self.thb_label)
        content_layout.addWidget(self.rub_label)
        content_layout.addWidget(self.myr_label)
        content_layout.addWidget(self.nzd_label)
        
        # 更新时间标签
        self.update_time_label = QLabel()
        self.update_time_label.setStyleSheet('color: #888888; font-size: 11px;')
        self.update_time_label.setAlignment(Qt.AlignCenter)
        self.update_time_label.setContentsMargins(15, 10, 15, 5)
        content_layout.addWidget(self.update_time_label)
        
        # 设置滚动区域
        scroll_area.setWidget(content_widget)
        
        # 添加所有组件到主布局
        main_layout.addWidget(title_bar)
        main_layout.addWidget(scroll_area)
        
        self.central_widget.setLayout(main_layout)
        
        # 设置固定宽度和高度
        self.setFixedWidth(300)
        self.setFixedHeight(450)
        
        # 初始更新汇率
        self.update_rates(True)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # 添加锁定位置选项
        lock_action = QAction("锁定位置" if not self.is_position_locked else "解锁位置", self)
        lock_action.triggered.connect(self.toggle_position_lock)
        menu.addAction(lock_action)
        
        # 添加置顶/取消置顶选项
        top_action = QAction("取消置顶" if self.is_top_most else "置顶窗口", self)
        top_action.triggered.connect(self.toggle_top_most)
        menu.addAction(top_action)
        
        # 添加开机自启动选项
        auto_start_action = QAction("开机自启" if not self.is_auto_start else "取消自启", self)
        auto_start_action.triggered.connect(self.toggle_auto_start)
        menu.addAction(auto_start_action)
        
        menu.addSeparator()
        
        # 添加最小化选项
        minimize_action = QAction("最小化", self)
        minimize_action.triggered.connect(self.showMinimized)
        menu.addAction(minimize_action)
        
        # 添加关闭选项
        close_action = QAction("关闭", self)
        close_action.triggered.connect(self.close)
        menu.addAction(close_action)
        
        menu.exec(event.globalPos())

    def toggle_top_most(self):
        self.is_top_most = not self.is_top_most
        flags = self.windowFlags()
        if self.is_top_most:
            flags |= Qt.WindowStaysOnTopHint
            self.top_most_btn.setText("置顶")
        else:
            flags &= ~Qt.WindowStaysOnTopHint
            self.top_most_btn.setText("普通")
        self.setWindowFlags(flags)
        self.show()
        self.top_most_btn.setChecked(self.is_top_most)
    
    def toggle_position_lock(self):
        self.is_position_locked = not self.is_position_locked
        self.lock_pos_btn.setChecked(self.is_position_locked)
        if self.is_position_locked:
            self.lock_pos_btn.setText("解锁")
        else:
            self.lock_pos_btn.setText("锁定")
        
        # 如果锁定，保存当前位置
        if self.is_position_locked:
            self.savePosition()
        
    def toggle_auto_start(self):
        new_state = not self.is_auto_start
        success = autostart_helper.set_auto_start(new_state)
        if success:
            self.is_auto_start = new_state
            status = "启用" if new_state else "禁用"
            self.update_time_label.setText(f"已{status}开机自启动")
            self.update_time_label.repaint()
        else:
            QMessageBox.warning(self, "权限不足", 
                            "设置开机自启动失败，可能需要管理员权限。\n请尝试以管理员身份运行程序。")
        
    def loadSettings(self):
        pos = self.settings.value("windowPosition")
        if pos:
            self.move(pos)
        
        # 加载锁定状态
        lock_state = self.settings.value("positionLocked", False, type=bool)
        self.is_position_locked = lock_state
        self.lock_pos_btn.setChecked(self.is_position_locked)
        if self.is_position_locked:
            self.lock_pos_btn.setText("解锁")
        else:
            self.lock_pos_btn.setText("锁定")
    
    def savePosition(self):
        self.settings.setValue("windowPosition", self.pos())
        self.settings.setValue("positionLocked", self.is_position_locked)
        
    def closeEvent(self, event):
        # 关闭前保存位置
        self.savePosition()
        super().closeEvent(event)
        
    def update_rates(self, force_refresh=False):
        try:
            # 更新状态显示
            if force_refresh:
                self.update_time_label.setText('正在更新数据...')
                self.update_time_label.repaint()  # 强制重绘
                
            # 获取贵金属价格
            metals_data = self.data_fetcher.get_metals_data()
            if metals_data:
                # 更新贵金属显示
                self.gold_label.setText(f'黄金: {metals_data["gold"]["BP"]} - {metals_data["gold"]["SP"]} 元/克')
                self.silver_label.setText(f'白银: {metals_data["silver"]["BP"]} - {metals_data["silver"]["SP"]} 元/克')
                self.platinum_label.setText(f'铂金: {metals_data["platinum"]["BP"]} - {metals_data["platinum"]["SP"]} 元/克')
                self.palladium_label.setText(f'钯金: {metals_data["palladium"]["BP"]} - {metals_data["palladium"]["SP"]} 元/克')
                
                # 更新时间
                self.update_time_label.setText(f'更新时间: {metals_data["update_time"]}')
            
            # 获取货币汇率
            forex_data = self.data_fetcher.get_forex_data(force_refresh)
            if forex_data:
                # 更新货币汇率显示，使用等宽数字字体
                def format_currency(code, name, rate):
                    try:
                        value = 100/forex_data[rate]
                        return f'{name}: 100 {rate} ≈ {value:.4f} CNY'
                    except KeyError:
                        return f'{name}: 数据不可用'
                
                # 主要货币
                self.usd_label.setText(format_currency('USD', '美元', 'USD'))
                self.eur_label.setText(format_currency('EUR', '欧元', 'EUR'))
                self.gbp_label.setText(format_currency('GBP', '英镑', 'GBP'))
                self.jpy_label.setText(format_currency('JPY', '日元', 'JPY'))
                self.hkd_label.setText(format_currency('HKD', '港币', 'HKD'))
                
                # 其他货币
                self.cad_label.setText(format_currency('CAD', '加元', 'CAD'))
                self.aud_label.setText(format_currency('AUD', '澳元', 'AUD'))
                self.chf_label.setText(format_currency('CHF', '瑞士法郎', 'CHF'))
                self.sgd_label.setText(format_currency('SGD', '新加坡元', 'SGD'))
                self.krw_label.setText(format_currency('KRW', '韩元', 'KRW'))
                self.thb_label.setText(format_currency('THB', '泰铢', 'THB'))
                self.rub_label.setText(format_currency('RUB', '俄罗斯卢布', 'RUB'))
                self.myr_label.setText(format_currency('MYR', '马来西亚林吉特', 'MYR'))
                self.nzd_label.setText(format_currency('NZD', '新西兰元', 'NZD'))
            
        except Exception as e:
            print(f"更新价格时出错: {e}")
            self.update_time_label.setText('更新失败，请检查网络连接')
    
    def mousePressEvent(self, event: QMouseEvent):
        if not self.is_position_locked and event.button() == Qt.LeftButton:
            self.oldPos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.is_position_locked and self.oldPos:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint() 