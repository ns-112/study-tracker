import numpy as np
import cv2

cap = cv2.VideoCapture(0) #Change the value to switch between different webcams/video sources

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_casade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


while True:
    ret, frame = cap.read() #Look at the frame from the webcam

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert the frame to grey scale
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #Arguments ( , scalefactor (larger faster less accurate, smaller slower more accurate), minNeighbors (How accurate, higher more accurate), minSize, Maxsize, maximum/minimum size of the face this could be useful for our implpementation)
    #finds all of the faces in the frame

    
    for(x, y, w, h) in faces: #draws rectangle around our detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5) #(255,0 , 0) IS COLOR, 5 IS LINE THICKNESS
        roi_gray = gray[y:y+w, x:x+w] #Finds the area of the face in the frame 
        roi_color = frame[y:y+h, x:x+w] 
        eyes = eye_casade.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes: 
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()