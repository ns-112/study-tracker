
import cv2 as cv
import dlib
import numpy as np
import pygame
import os

def eyeDetection():
    
    src_dir = os.path.dirname(os.path.abspath(__file__))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.path.join(src_dir,"shape_predictor_68_face_landmarks.dat"))


    cam = cv.VideoCapture(0)
    while True:
        ret,frame = cam.read()
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)
        faces=detector(gray)
        if (len(faces) == 0):
            cv.putText(frame, str("No Face Detected"), (125, 100), 5, 2, (255, 255, 255), 2)
        for face in faces:
            landmarks= predictor(gray,face)
            height,width, _= frame.shape
            mask = np.zeros((height,width), np.uint8)
            leftEyeRegion = np.array([(landmarks.part(36).x,landmarks.part(36).y),
                                      (landmarks.part(37).x,landmarks.part(37).y),
                                      (landmarks.part(38).x,landmarks.part(38).y),
                                      (landmarks.part(39).x,landmarks.part(39).y),
                                      (landmarks.part(40).x,landmarks.part(40).y),
                                      (landmarks.part(41).x,landmarks.part(41).y)], np.int32)

            cv.polylines(mask, [leftEyeRegion], True, 255, 2)
            cv.fillPoly(mask, [leftEyeRegion], 255)
            eyes = cv.bitwise_and(gray, gray, mask=mask)
            min_x = np.min(leftEyeRegion[:, 0])
            max_x = np.max(leftEyeRegion[:, 0])
            min_y = np.min(leftEyeRegion[:, 1])
            max_y = np.max(leftEyeRegion[:, 1])
            gray_eye = eyes[min_y: max_y, min_x: max_x]
            _, threshold = cv.threshold(gray_eye, 70, 255, cv.THRESH_BINARY)
            height,width = threshold.shape
            leftSideThreshold = threshold[0: height, 0: int(width/2)]
            leftSideWhite = cv.countNonZero(leftSideThreshold)
            rightSideThreshold = threshold[0: height, int(width/2): width]
            rightSideWhite = cv.countNonZero(rightSideThreshold)
            threshold = cv.resize(threshold, None, fx=5, fy=5)
            if (rightSideWhite == 0):
                gazeRation = 1
            else:
                gazeRation = leftSideWhite/rightSideWhite

            if (gazeRation > 3):
                cv.putText(frame, str("Looking Left"), (125, 100), 5, 2, (255, 255, 255), 2)
            elif (gazeRation < 1):
                cv.putText(frame, str("Looking Right"), (125, 100), 5, 2, (255, 255, 255), 2)
            else:
                cv.putText(frame, str("Looking Center"), (125, 100), 5, 2, (255, 255, 255), 2)


        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        frame_rgb = np.flipud(frame_rgb)
        yield pygame.surfarray.make_surface(frame_rgb)

            

        if cv.waitKey(1) == ord('q'):
            break
    cam.release()
