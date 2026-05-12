from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy, QScrollArea, QGraphicsDropShadowEffect
from PyQt6.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat, QLinearGradient, QBrush, QFontDatabase
from PyQt6.QtCore import Qt, QSize, QTimer, QRect, QPropertyAnimation, QEasingCurve, QPoint
from dotenv import dotenv_values
import sys
import os
import random

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Jarvis")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

# Custom Styles - Premium OMNI Dark Mode
MODERN_STYLE = """
    QWidget {
        background-color: #050505;
        color: #F0F0F0;
        font-family: 'Space Grotesk', 'Inter', 'Segoe UI', sans-serif;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 4px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #222;
        min-height: 20px;
        border-radius: 2px;
    }
    QScrollBar::handle:vertical:hover {
        background: #007AFF;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def SetMicroPhoneStatus(Command):
    with open(os.path.join(TempDirPath, "Mic.data"), "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicroPhoneStatus():
    with open(os.path.join(TempDirPath, "Mic.data"), "r", encoding='utf-8') as file:
        return file.read()

def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(os.path.join(TempDirPath, "Status.data"), "r", encoding='utf-8') as file:
        return file.read()

def get_graphics_path(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def get_temp_path(Filename):
    return os.path.join(TempDirPath, Filename)

def ShowTextToScreen(Text):
    with open(os.path.join(TempDirPath, "Responses.data"), "w", encoding='utf-8') as file:
        file.write(Text)

# Voice Visualizer Widget
class VoiceVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setFixedWidth(160)
        self.bars = [random.randint(5, 20) for _ in range(12)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_bars)
        self.active = False

    def start(self):
        self.active = True
        self.timer.start(60)

    def stop(self):
        self.active = False
        self.timer.stop()
        self.bars = [4 for _ in range(12)]
        self.update()

    def animate_bars(self):
        if self.active:
            self.bars = [random.randint(5, 35) for _ in range(12)]
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        spacing = 6
        bar_width = 6
        
        for i, h in enumerate(self.bars):
            gradient = QLinearGradient(0, 0, 0, 40)
            gradient.setColorAt(0, QColor("#007AFF"))
            gradient.setColorAt(1, QColor("#00BFFF"))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            
            x = i * (bar_width + spacing)
            y = (40 - h) // 2
            painter.drawRoundedRect(x, y, bar_width, h, 3, 3)

class ChatBubble(QFrame):
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        
        self.container = QFrame()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 10, 15, 10)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(700)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        if is_user:
            self.container.setStyleSheet("""
                background-color: #121214;
                color: #FFFFFF;
                border: 1px solid #222;
                border-radius: 15px;
                border-bottom-right-radius: 2px;
                font-size: 14px;
            """)
            layout.addStretch()
            layout.addWidget(self.container)
        else:
            self.container.setStyleSheet("""
                background-color: #007AFF;
                color: #FFFFFF;
                border-radius: 15px;
                border-bottom-left-radius: 2px;
                font-size: 14px;
            """)
            layout.addWidget(self.container)
            layout.addStretch()
            
        self.container_layout.addWidget(self.label)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.container.setGraphicsEffect(shadow)

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 10)
        
        # OMNI Header
        header = QHBoxLayout()
        omni_title = QLabel("OMNI INTELLIGENCE CORE")
        omni_title.setStyleSheet("font-size: 9px; font-weight: 900; color: #444; letter-spacing: 4px;")
        self.visualizer = VoiceVisualizer()
        header.addWidget(omni_title)
        header.addStretch()
        header.addWidget(self.visualizer)
        self.layout.addLayout(header)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.chat_layout = QVBoxLayout(self.scroll_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(8)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        
        # Stats Bar
        self.stats_bar = QFrame()
        self.stats_bar.setFixedHeight(60)
        stats_layout = QHBoxLayout(self.stats_bar)
        
        self.sys_info = QLabel("SYSTEM: SECURE | LINK: ACTIVE | SYNC: 100%")
        self.sys_info.setStyleSheet("font-size: 10px; color: #222; font-weight: bold; letter-spacing: 1px;")
        
        self.gif_label = QLabel()
        self.movie = QMovie(get_graphics_path('Jarvis.gif'))
        self.movie.setScaledSize(QSize(100, 56))
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        
        self.status_label = QLabel("INITIALIZING...")
        self.status_label.setStyleSheet("font-size: 11px; color: #007AFF; font-weight: 800; letter-spacing: 2px;")
        
        stats_layout.addWidget(self.sys_info)
        stats_layout.addStretch()
        stats_layout.addWidget(self.status_label)
        stats_layout.addSpacing(10)
        stats_layout.addWidget(self.gif_label)
        self.layout.addWidget(self.stats_bar)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(200)

    def add_bubble(self, text, is_user=True):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.addWidget(bubble)
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def loadMessages(self):
        global old_chat_message
        try:
            with open(get_temp_path('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read().strip()
                if messages and messages != old_chat_message:
                    is_user = messages.startswith(env_vars.get("username", "User"))
                    self.add_bubble(messages, is_user=is_user)
                    old_chat_message = messages
        except:
            pass

    def updateStatus(self):
        try:
            status = GetAssistantStatus().upper()
            self.status_label.setText(status)
            if any(s in status for s in ["LISTENING", "THINKING", "SEARCHING", "ANSWERING"]):
                self.visualizer.start()
            else:
                self.visualizer.stop()
        except:
            pass

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QFrame()
        self.container.setStyleSheet("background-color: #050505;")
        container_layout = QVBoxLayout(self.container)
        
        self.gif_label = QLabel()
        self.movie = QMovie(get_graphics_path('Jarvis.gif'))
        self.movie.setScaledSize(QSize(800, 450))
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        
        self.mic_btn = QPushButton()
        self.mic_btn.setFixedSize(140, 140)
        self.mic_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #007AFF, stop:1 #002A55);
                border-radius: 70px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            QPushButton:hover { background-color: #007AFF; }
        """)
        self.update_mic_icon(True)
        self.mic_btn.clicked.connect(self.toggle_mic)
        
        self.name_label = QLabel(Assistantname.upper())
        self.name_label.setStyleSheet("font-size: 64px; font-weight: 900; letter-spacing: 25px; color: #FFF; margin-left: 20px;")
        
        self.status_txt = QLabel("OMNI PASSIVE OVERWATCH ACTIVE")
        self.status_txt.setStyleSheet("font-size: 11px; color: #333; letter-spacing: 6px; font-weight: bold;")
        
        container_layout.addStretch()
        container_layout.addWidget(self.gif_label, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addSpacing(40)
        container_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.status_txt, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addSpacing(60)
        container_layout.addWidget(self.mic_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        container_layout.addStretch()
        
        layout.addWidget(self.container)
        
        self.toggled = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(250)

    def update_mic_icon(self, active):
        icon_path = get_graphics_path('Mic_on.png' if active else 'Mic_off.png')
        self.mic_btn.setIcon(QIcon(icon_path))
        self.mic_btn.setIconSize(QSize(50, 50))

    def toggle_mic(self):
        self.toggled = not self.toggled
        self.update_mic_icon(self.toggled)
        SetMicroPhoneStatus("True" if self.toggled else "False")

    def update_status(self):
        try:
            self.status_txt.setText(GetAssistantStatus().upper())
        except:
            pass

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.setFixedHeight(100)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(60, 0, 60, 0)
        
        logo = QLabel(f"OMNI")
        logo.setStyleSheet("font-size: 24px; font-weight: 900; color: #FFF; letter-spacing: 12px;")
        
        nav = QWidget()
        nav_layout = QHBoxLayout(nav)
        nav_layout.setSpacing(60)
        
        self.home_btn = QPushButton("CORE")
        self.chat_btn = QPushButton("INTERFACE")
        
        for btn in [self.home_btn, self.chat_btn]:
            btn.setFlat(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; 
                    border: none; 
                    font-size: 10px; 
                    font-weight: 900; 
                    color: #444; 
                    letter-spacing: 3px;
                }
                QPushButton:hover { color: #007AFF; }
            """)
        
        self.home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.chat_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.chat_btn)
        
        close_btn = QPushButton("EXIT")
        close_btn.setFixedSize(80, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #222;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                color: #444;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #FF3B30;
                color: white;
                border: none;
            }
        """)
        close_btn.clicked.connect(self.window().close)
        
        layout.addWidget(logo)
        layout.addStretch()
        layout.addWidget(nav)
        layout.addStretch()
        layout.addWidget(close_btn)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.init_ui()

    def init_ui(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setStyleSheet(MODERN_STYLE)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget()
        self.top_bar = CustomTopBar(self, self.stacked_widget)
        
        self.msg_screen = QWidget()
        msg_layout = QVBoxLayout(self.msg_screen)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        msg_layout.addWidget(ChatSection())
        
        self.stacked_widget.addWidget(InitialScreen())
        self.stacked_widget.addWidget(self.msg_screen)
        
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.stacked_widget)

def GraphicalUserInterface(on_start=None):
    app = QApplication(sys.argv)
    if on_start:
        on_start()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    GraphicalUserInterface()
