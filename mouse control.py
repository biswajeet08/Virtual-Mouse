import autopy
import cv2
import mediapipe as mp
from HandTracking import HandDetector
import numpy as np
from pynput.mouse import Button, Controller
from concurrent.futures import ThreadPoolExecutor as tpe

wCam, hCam = 1080, 720
frameR1, frameR2 = 200, 100
smoothening = 7
plocX, plocY, clocX, clocY = 0, 0, 0, 0
cap = cv2.VideoCapture(0)
detector = HandDetector(trackCon=0.6, maxHands=1)
wScreen, hScreen = autopy.screen.size()
mouse = Controller()



def mouse_button(lentgh2):
    mouse.press(Button.left)

    length2, cx2, cy2 = detector.findLength(img, 8, 12)
    if length2 > 50:
        mouse.release(Button.left)



while True:
    success, img = cap.read()
    img = cv2.resize(img, (wCam, hCam))
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # cv2.rectangle(img, (frameR1, frameR2), (wCam - frameR1, hCam - frameR2-150), (255, 0, 255), 2)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1:]
        x2, y2 = lmList[8][1:]
        x3, y3 = lmList[12][1:]
        fingersUp = detector.fingersUp(img)

        if fingersUp[1] == 1 and fingersUp[0] == 1 and fingersUp[2] == 1:
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            x3 = np.interp(x1, (frameR1, wCam - frameR1), (0, wScreen))
            y3 = np.interp(y1, (frameR2, hCam - frameR2-150), (0, hScreen))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            try:
                autopy.mouse.move(wScreen - clocX, clocY)
            except:
                pass
            plocX, plocY = clocX, clocY

            length1, cx1, cy1 = detector.findLength(img, 4, 8)
            length2, cx2, cy2 = detector.findLength(img, 8, 12)
            print(length2)
            if length1 < 40:
                cv2.circle(img, (cx1, cy1), 10, (255, 0, 0), cv2.FILLED)
                autopy.mouse.click()
            if length2 < 50:
                cv2.circle(img, (cx2, cy2), 10, (255, 0, 0), cv2.FILLED)
                mouse.press(Button.left)
                # length2, cx2, cy2 = detector.findLength(img, 8, 12)
                # if length2 > 50:
                #     mouse.release(Button.left)
            # if length2 > 50:
            #     mouse.release(Button.left)




        # print(fingersUp)
    cv2.imshow("Hand", img)
    if cv2.waitKey(1) == ord('q'):
        break
