import cv2
import time
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QImage, QPixmap
#from onnx_inference import image_main, movie_main


class RightUI(QWidget):
    def __init__(self, parent, opt):
        super(RightUI, self).__init__(parent)
        
        self.VideoWidget(opt)
        self.FPSbar()
        self.PredictedTimeBar()
        
    def VideoWidget(self, opt):
        self.video_widget = QLabel()
        self.video_size = QSize(int(opt.height/3), int(opt.width/3))
        self.video_widget.setFixedSize(self.video_size)
        
    def FPSbar(self):
        self.fps_layout = QHBoxLayout()
        self.fps_title = QLabel('Constant FPS')
        self.fps = QLabel('', self)
        self.fps.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.fps_layout.addWidget(self.fps_title)
        self.fps_layout.addWidget(self.fps)
    
    def PredictedTimeBar(self):
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Predicted time')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)

        
class RightCamWidget(QWidget):
    def __init__(self, parent, opt):
        super().__init__(parent=parent)
        
        self.parent = parent
        self.right_capture = cv2.VideoCapture(opt.video_path)
        
        self.W, self.H = opt.width, opt.height
        self.video_size = QSize(self.W, self.H)
        self.TIMEOUT = 1
        self.cur_fps = 0
        self.old_timestamp = time.time()
        self.setup_ui()
        self.setup_camera()
        self.plot_fps(initial=True)
        
    def setup_ui(self):
        """Initialize widgets.
        """
        self.set1_calcurate_bar_layout()
        self.set2_video_bar_layout()
        self.set3_main_layout()
        
    def set1_calcurate_bar_layout(self):
        # Predicted time bar
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Predicted time')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)

        # FPS bar
        self.fps_layout = QHBoxLayout()
        self.fps_title = QLabel('Constant FPS')
        self.fps = QLabel('', self)
        self.fps.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.fps_layout.addWidget(self.fps_title)
        self.fps_layout.addWidget(self.fps)
        
    def set2_video_bar_layout(self):
        # video widget
        self.video_widget = QLabel()
        self.video_widget.setFixedSize(self.video_size)
        
    def set3_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.addLayout(self.predictor_layout)
        self.main_layout.addLayout(self.fps_layout)
        self.setLayout(self.main_layout)
        
    def setup_camera(self):
        """Initialize camera.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, rframe = self.right_capture.read()
        fps = (time.time() - self.old_timestamp) / self.TIMEOUT
        if (time.time() - self.old_timestamp) > self.TIMEOUT:
            start = time.time()
            # right prediction
            right_pred_frame = rframe  #movie_main(self.onnx_path, rframe.copy())
            self.predict_time = np.round((time.time() - start), decimals=5)
            pred_frame = cv2.resize(right_pred_frame, (self.W, self.H))
            
            image = QImage(pred_frame, pred_frame.shape[1], pred_frame.shape[0],
                            pred_frame.strides[0], QImage.Format_RGB888)
            self.video_widget.setPixmap(QPixmap.fromImage(image))
            self.old_timestamp = time.time()
            
            self.cur_fps = np.round(fps, decimals=3)
            self.plot_fps()
        
    def plot_fps(self, initial=None):
        if initial:
            self.fps.setText("now loading")
        else:
            self.fps.setText(str(self.cur_fps))
            self.predictbar.setText(str(self.predict_time*1000)+"[ms]")
