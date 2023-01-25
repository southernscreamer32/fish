from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

max_value = 255
max_value_H = 360 // 2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()
cap = cv.VideoCapture(args.camera)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)
params = cv.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 155
params.maxThreshold = 255

# random filters we dont care about
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

# see white blobs
params.filterByColor = True
params.blobColor = 255

# ignore small blobs
params.filterByArea = True
params.minArea = 500
params.maxArea = 50000

while True:

    ret, frame = cap.read()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    frame_threshold = cv.inRange(frame_HSV, (80, 140, 60), (150, 255, 255))
    ver = (cv.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv.SimpleBlobDetector(params)
    else:
        detector = cv.SimpleBlobDetector_create(params)
    # detector = cv.SimpleBlobDetector()
    # Detect blobs.
    keypoints = detector.detect(frame_threshold)
    # Draw detected blobs as red circles.
    if len(keypoints) > 0:
        # print(keypoints[0].pt)
        if keypoints[0].pt[0] > 500 and keypoints[0].pt[1] > 500:
            print('fish gaming!!!!!!!!')
        else:
            print('not gaming!!!!!!')
    else:
        print('no fish....')
    # print(keypoints[0])
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                         cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Show keypoints

    # print(keypoints)

    cv.imshow(window_capture_name, im_with_keypoints)
    cv.imshow(window_detection_name, frame_threshold)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break