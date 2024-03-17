from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QLabel, QSizePolicy, QSpacerItem
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QImage, QPixmap
import time
import cv2
import numpy as np

class LeftWidget(QWidget):
    def __init__(self, parent, opt, cap = None, ):
        super(LeftWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.cap = cap
        self.video_size = QSize(opt.Leftwidget_size, opt.Leftwidget_size)
        self.TIMEOUT = 1
        self.cur_fps = 0
        self.old_timestamp = time.time()
        
        # left uuper parts
        self.scene_brush = QLabel('')
        self.gview_brush = QGraphicsView(self.scene_brush, self)
        self.gview_brush.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.gview_brush.setMinimumSize(256, 50)
        self.layout.addWidget(self.gview_brush)

        self.setup_camera()
        self.setUI()
            
    def setUI(self):
        # video space
        self.video_space = QLabel()
        self.video_space.setFixedSize(self.video_size)
        self.layout.addWidget(self.video_space)

        # FPS bar
        self.fps_layout = QHBoxLayout()
        self.fps_title = QLabel('Normal FPS')
        self.fps = QLabel('', self)
        self.fps.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')

        self.fps_layout.addWidget(self.fps_title)
        self.fps_layout.addWidget(self.fps)
        self.layout.addLayout(self.fps_layout)

        # スペーシング
        spc = QSpacerItem(16, 16, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addSpacerItem(spc)

        # 自身のレイアウトとして設定
        self.setLayout(self.layout)
        
        
    def setup_camera(self):
        """Initialize camera.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.cap.read()
        fps = (time.time() - self.old_timestamp) / self.TIMEOUT
        if (time.time() - self.old_timestamp) > self.TIMEOUT:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_ = cv2.resize(frame, (200, 200))
            image = QImage(frame_, frame_.shape[1], frame_.shape[0],
                           frame_.strides[0], QImage.Format_RGB888)
            self.video_space.setPixmap(QPixmap.fromImage(image))
            self.old_timestamp = time.time()
        
            self.cur_fps = np.round(fps, decimals=3)
            self.plot_bar()
            
    def plot_bar(self):
        self.fps.setText(str(self.cur_fps))

