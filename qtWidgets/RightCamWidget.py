import cv2, os
import numpy as np
import time
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize

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
        
    def plot_fps(self, initial=None):
        if initial:
            self.fps.setText("now loading")
        else:
            self.fps.setText(str(self.cur_fps))
            self.predictbar.setText(str(self.predict_time*1000)+"[ms]")


        
        
class RightCamWidget(QWidget):
    def __init__(self, parent, opt):
        super().__init__(parent=parent)
        
        self.parent = parent
        self.RUI = RightUI(self, opt)
        self.cap, out_frame, frame_width, frame_height = self.get_cap(opt)
        
        # video wiget
        #self.size = 500
        #self.video_size = QSize(self.size*2, self.size)
        #self.video_widget = QLabel()
        #self.video_widget.setFixedSize(self.video_size)
        
        
        #self.TIMEOUT = 1
        #self.cur_fps = 0
        #self.onnx_path = onnx_path
        #self.old_timestamp = time.time()
        self.setup_ui(opt)
        #self.setup_camera()
        
    def setup_ui(self, opt):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.RUI.plot_fps(initial=True)
        self.main_layout.addWidget(self.RUI.video_widget)
        self.main_layout.addLayout(self.RUI.predictor_layout)
        self.main_layout.addLayout(self.RUI.fps_layout)

    def get_cap(self, opt):
        cap = cv2.VideoCapture(opt.right_video_path)
        if not cap.isOpened():
            print('can not open video')
            exit()
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))  # FPS
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_frame = cv2.VideoWriter(opt.output_file+"_onnx.mp4", fourcc, fps, (frame_width, frame_height), isColor=False)
        return cap, out_frame, frame_width, frame_height
        
    """
    def setup_ui(self):
        
        self.set1_calcurate_bar_layout()
        self.set2_video_bar_layout()
    
        
        
    #def set3_main_layout(self):
        
        #self.main_layout.addWidget(self.video_widget)
    
    def setup_camera(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        
        _, rframe = self.right_capture.read()
        fps = (time.time() - self.old_timestamp) / self.TIMEOUT
        if (time.time() - self.old_timestamp) > self.TIMEOUT:
            start = time.time()
            # right prediction
            right_pred_frame = movie_main(self.onnx_path, rframe.copy())
            self.predict_time = np.round((time.time() - start), decimals=5)
            pred_frame = cv2.resize(right_pred_frame, (self.size, self.size*2))
            
            image = QImage(pred_frame, pred_frame.shape[0], pred_frame.shape[1],
                            pred_frame.strides[0], QImage.Format_RGB888)
            self.video_widget.setPixmap(QPixmap.fromImage(image))
            self.old_timestamp = time.time()
            
            self.cur_fps = np.round(fps, decimals=3)
            self.plot_fps()
            
    """
    def return_cap(self):
        return self.cap
        
    
