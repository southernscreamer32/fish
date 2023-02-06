#opencv is MIT
import cv2

# Read image
cam = cv2.VideoCapture(0)

while(1):
        ret, frame = cam.read()

        if not ret:
            break

        canvas = frame.copy()

        lower = (80,0,0)  #130,150,80
        upper = (255,200,200) #250,250,120
        mask = cv2.inRange(frame, lower, upper)
        try:
            # NB: using _ as the variable name for two of the outputs, as they're not used
            _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            blob = max(contours, key=lambda el: cv2.contourArea(el))
            M = cv2.moments(blob)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            cv2.circle(canvas, center, 2, (0,0,255), -1)

        except (ValueError, ZeroDivisionError):
            pass

        cv2.imshow('frame',frame)
        cv2.imshow('canvas',canvas)
        cv2.imshow('mask',mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
im.release()
cv2.destroyAllWindows()