from PyQt6.QtWidgets import QWidget, QVBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

import cv2
from numpy import array, ndarray

class Camera(QLabel):
    def __init__(self, port):
        super().__init__()

        self.thread = VideoThread(port)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def close_event(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(720, 480, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, port):
        super().__init__()

        self.running = True
        self.port = port

        self.params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        self.params.minThreshold = 155
        self.params.maxThreshold = 255

        # random filters we dont care about
        self.params.filterByCircularity = False
        self.params.filterByConvexity = False
        self.params.filterByInertia = False

        # see white blobs
        self.params.filterByColor = True
        self.params.blobColor = 255

        # ignore small blobs
        self.params.filterByArea = True
        self.params.minArea = 500
        self.params.maxArea = 50000

    def run(self):
        cap = cv2.VideoCapture(self.port)

        while self.running:
            ret, image = cap.read()

            if ret:
                image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                image_threshold = cv2.inRange(image_HSV, (80, 140, 60), (150, 255, 255))

                detector = cv2.SimpleBlobDetector_create(self.params)

                keypoints = detector.detect(image_threshold)

                if len(keypoints) > 0:
                    if keypoints[0].pt[0] > 500 and keypoints[0].pt[1] > 500:
                        # print('fish gaming!!!!!!!!')
                        pass
                    else:
                        # print('not gaming!!!!!!')
                        pass
                else:
                    # print('no fish....')
                    pass

                im_with_keypoints = cv2.drawKeypoints(image, keypoints, array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                

                self.change_pixmap_signal.emit(im_with_keypoints)
                
        cap.release()
        
    def stop(self):
        self.running = False
        self.wait()

