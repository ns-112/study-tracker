import cv2
cap = cv2.VideoCapture('out.avi')
while cap.isOpened:
    ret,frame = cap.read()
    if ret:
        cv2.imshown(frame)

