import argparse
import sys
import os
#from yolov7s.common import obdetect_inference
#from midas.midas_utils import call_transform, midas_onnx_prediction
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QDockWidget
from qtWidgets.RightCamWidget import RightCamWidget
from qtWidgets.LeftWidget import LeftWidget

class MyMainWindow(QMainWindow):
    def __init__(self, opt, parent=None):
        super(MyMainWindow, self).__init__(parent)
        
        # RIGHT Side camera widget
        here_path = os.path.dirname(os.path.abspath(__file__))
        self.plot_layout = QVBoxLayout()
        self.right_video_path = os.path.join(here_path, opt.right_video_path)
        self.right_widget = RightCamWidget(self, opt)
        self.plot_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.right_widget)
    
        
        # Left side widget
        cap = self.right_widget.return_cap()
        self.leftDock = QDockWidget("Left Widget", self)
        self.leftside = LeftWidget(self, cap)
        self.leftDock.setWidget(self.leftside)
 
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea
                                   | Qt.RightDockWidgetArea)
        self.leftDock.setFeatures(QDockWidget.DockWidgetMovable
                                  | QDockWidget.DockWidgetFloatable)
        #self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)
        
        
def main(opt):
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('Cleanlooks'))
    w = MyMainWindow(opt)
    w.setWindowTitle("PySide Layout on QMainWindow")
    w.resize(opt.width, opt.height)
    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolov7_onnx_path', type=str, default='weights/yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--midas_onnx_path', type=str, default='weights/model-f6b98070.onnx', help='onnx midas weight model')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--right_video_path', type=str, default='data/outdriving.mov', help='right video path')
    parser.add_argument('-o', '--output_file', type=str, default='data/movie', help='movie output path')
    parser.add_argument('--height', type=int, default=500, help='height of movie')
    parser.add_argument('--width', type=int, default=1200, help='width of of movie')
    #parser.add_argument('-s', '--show', action='store_true', help='prepare test data')
    opt = parser.parse_args()
    try:
        main(opt)
    except KeyboardInterrupt:
        sys.exit(1)
        raise
