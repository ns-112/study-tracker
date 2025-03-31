import cv2 as cv
import dlib
import os
import numpy as np
import pygame

def eyeDetection():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(src_dir)
    source_dir = f'{project_dir}\\src\\'

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(f"{source_dir}shape_predictor_68_face_landmarks.dat")

    cam = cv.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)
        faces = detector(gray)

       

        for face in faces:
          
            landmarks = predictor(gray, face)
            
            left_eye_points = [landmarks.part(i) for i in range(36, 42)]
            right_eye_points = [landmarks.part(i) for i in range(42, 48)]

           
            left_eye_center = np.mean([(p.x, p.y) for p in left_eye_points], axis=0).astype(int)
            right_eye_center = np.mean([(p.x, p.y) for p in right_eye_points], axis=0).astype(int)

           
            cv.circle(frame, tuple(left_eye_center), 10, (0, 255, 0), -1) 
            cv.circle(frame, tuple(right_eye_center), 10, (0, 255, 0), -1) 

       
            eye_surface_left = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(eye_surface_left, (0, 255, 0), (2, 2), 2)  
            eye_surface_right = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(eye_surface_right, (0, 255, 0), (2, 2), 2)  
           
            

           
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

       
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        
       
        yield frame_surface

    cam.release()
