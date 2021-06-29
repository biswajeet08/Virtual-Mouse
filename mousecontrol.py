import autopy
import cv2
import numpy as np
from HandTracking import HandDetector
from pynput.mouse import Button, Controller


class VirtualMouse():
    def __init__(self, cam_no=0, wCam=1080, hCam=720, fingers=[4, 8, 12], frameR1=200, frameR2=100, smoothening=7):
        self.cam_no = cam_no
        self.wCam, self.hCam = wCam, hCam
        self.frameR1, self.frameR2 = frameR1, frameR2
        self.smoothening = smoothening
        self.plocX, self.plocY, self.clocX, self.clocY = 0, 0, 0, 0
        self.detector = HandDetector(trackCon=0.6, maxHands=1)
        self.wScreen, self.hScreen = autopy.screen.size()
        self.mouse = Controller()
        self.fingers_dict = {4: 0, 8: 1, 12: 2, 16: 3, 20: 4}
        self.fingers = fingers

    def mouse_control(self):
        cap = cv2.VideoCapture(self.cam_no)
        while True:
            success, img = cap.read()
            img = cv2.resize(img, (self.wCam, self.hCam))
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img, draw=False)
            # cv2.rectangle(img, (frameR1, frameR2), (wCam - frameR1, hCam - frameR2-150), (255, 0, 255), 2)
            if len(lmList) != 0:
                x1, y1 = lmList[self.fingers[0]][1:]
                x2, y2 = lmList[self.fingers[1]][1:]
                x3, y3 = lmList[self.fingers[2]][1:]
                fingersUp = self.detector.fingersUp(img)

                if fingersUp[self.fingers_dict.get(self.fingers[0])] == 1 and \
                        fingersUp[self.fingers_dict.get(self.fingers[1])] == 1 and \
                        fingersUp[self.fingers_dict.get(self.fingers[2])] == 1:
                    cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                    x3 = np.interp(x1, (self.frameR1, self.wCam - self.frameR1), (0, self.wScreen))
                    y3 = np.interp(y1, (self.frameR2, self.hCam - self.frameR2 - 150), (0, self.hScreen))
                    self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
                    self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
                    try:
                        autopy.mouse.move(self.wScreen - self.clocX, self.clocY)
                    except:
                        pass
                    self.plocX, self.plocY = self.clocX, self.clocY

                    length1, cx1, cy1 = self.detector.findLength(img, 4, 8)
                    length2, cx2, cy2 = self.detector.findLength(img, 8, 12)
                    print(length2)
                    if length1 < 40:
                        cv2.circle(img, (cx1, cy1), 10, (255, 0, 0), cv2.FILLED)
                        autopy.mouse.click()
                    if length2 < 50:
                        cv2.circle(img, (cx2, cy2), 10, (255, 0, 0), cv2.FILLED)
                        self.mouse.press(Button.left)

            cv2.imshow("Hand", img)
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == '__main__':
    virtual_mouse = VirtualMouse()
    virtual_mouse.mouse_control()
