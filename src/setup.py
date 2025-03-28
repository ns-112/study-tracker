def eyeDetection():
    import cv2 as cv
    import dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    color=(0,255,0)
    thickness=2

    cam = cv.VideoCapture(0)
    while True:
        ret,frame = cam.read()
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)
        faces=detector(gray)
        for face in faces:
            x,y = face.left(), face.top()
            w, h = face.right(), face.bottom()
            cv.rectangle(frame, (x,y), (w,h),color, thickness)

            landmarks= predictor(gray,face)

            rightEye_midpoint = int((landmarks.part(43).x + landmarks.part(46).x)/2), int((landmarks.part(43).y + landmarks.part(46).y)/2)
            leftEye_midpoint = int((landmarks.part(36).x + landmarks.part(39).x)/2), int((landmarks.part(36).y + landmarks.part(39).y)/2)
            cv.circle(frame, leftEye_midpoint, 1, color, thickness) 
            cv.circle(frame, rightEye_midpoint, 1, color, thickness)
        cv.imshow('Camera',frame)

        if cv.waitKey(1) == ord('q'):
            break
    cam.release()
    cv.destroyAllWindows()
