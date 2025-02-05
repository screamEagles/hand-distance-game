import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import random
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coefficient = np.polyfit(x, y, 2)  # y = ax^2 + bx + c

# game variables
centre_x, centre_y = 250, 250
colour = (245, 222, 105)
counter = 0
score = 0
time_start = time.time()
total_time =  20

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if time.time() - time_start < total_time:
        hands = detector.findHands(img, draw=False)

        if hands:
            landmark_list = hands[0]['lmList']
            # print(landmark_list)

            x, y, w, h = hands[0]['bbox']
            x1, y1 = landmark_list[5]
            x2, y2 = landmark_list[17]
        
            # pythagoras theorem is used because (x2 - x1) will give incomplete data
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))

            # polynomial function is used for centimetres conversion because the x-y relationship is not linear
            a, b, c = coefficient
            distance_centimetres = a * distance ** 2 + b * distance + c
            # print(distance_centimetres, distance)

            if distance_centimetres < 40:
                if x < centre_x < x + w and y < centre_y < y + h:
                    counter = 1            

            cv2.rectangle(img, (x, y), (x + w, y + h), colour, 3)
            cvzone.putTextRect(img, f"{int(distance_centimetres)}", (x + 5, y - 10))

        if counter:
            counter += 1
            colour = (30, 255, 0)
            if counter == 3:
                centre_x = random.randint(100, 1100)
                centre_y = random.randint(100, 600)
                colour = (245, 222, 105)
                score += 1
                counter = 0



        # draw button
        cv2.circle(img, (centre_x, centre_y), 30, colour, cv2.FILLED)
        cv2.circle(img, (centre_x, centre_y), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (centre_x, centre_y), 20, (255, 255, 255), 2)
        cv2.circle(img, (centre_x, centre_y), 30, (0, 0, 0), 2)

        # game HUD
        cvzone.putTextRect(img, f"Time: {int(total_time - (time.time() - time_start))}", (1000, 75), scale=3, offset=20)
        cvzone.putTextRect(img, f"Score: {str(score).zfill(2)}", (60, 75), scale=3, offset=20)
    else:
        cvzone.putTextRect(img, "Game Over", (400, 400), scale=5, offset=30, thickness=7)
        cvzone.putTextRect(img, f"Your Score {score}", (450, 500), scale=3, offset=20)
        cvzone.putTextRect(img, "Press R To Restart, Q To Quit", (375, 575), scale=2, offset=10)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        time_start = time.time()
        score = 0
    if key == ord('q'):
        break