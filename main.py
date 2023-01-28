import cv2
import numpy as np

cap = cv2.VideoCapture('short.mov')

n_dets = 0

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = img[800:1500]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 19)

    circles = cv2.HoughCircles(
        blur,
        method=cv2.HOUGH_GRADIENT,
        dp=1,         # 테스트 필요
        minDist=50,   # 여러 원이 탐지되었을때 원간의 최소 거리
        param1=100,   # 값이 클수록 판단기준 엄격해짐
        param2=35,    # 값이 클수록 판단기준 엄격해짐
        minRadius=70, # 최소 원 크기
        maxRadius=100 # 최대 원 크기
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        # print(circles)

        for circle in circles[0, :]:
            cv2.circle(img, (circle[0], circle[1]) ,circle[2], (255, 0, 255), 5)
            cv2.putText(img, text=f'{circle[2]}', org=(circle[0], circle[1] - circle[2]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(255, 0, 255), thickness=3)

            if 65 < circle[2] < 80:
                n_dets += 1
                if n_dets > 10:
                    cv2.putText(img, text=f'Ready!', org=(circle[0], circle[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=5)
            else:
                n_dets = 0

    cv2.imshow('blur', blur)
    cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break
