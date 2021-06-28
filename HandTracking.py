import cv2
import mediapipe as mp
import math


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detection=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detection = detection
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detection, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def fingersUp(self, img):
        tipIds = [4, 8, 12, 16, 20]
        lmlist = self.findPosition(img, draw=False)

        if len(lmlist) != 0:
            fingersUp = []
            if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
                fingersUp.append(1)
            else:
                fingersUp.append(0)
            for id in range(1, 5):
                if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 1][2]:
                    fingersUp.append(1)
                else:
                    fingersUp.append(0)
            return fingersUp

    def findLength(self, img, point1, point2):
        lmList = self.findPosition(img)
        if len(lmList) != 0:
            x1, y1 = lmList[point1][1], lmList[point1][2]
            x2, y2 = lmList[point2][1], lmList[point2][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            return length, cx, cy


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(trackCon=0.7, maxHands=1)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        fingersUp = detector.fingersUp(img)
        # print(fingersUp)
        length = detector.findLength(img, 4, 8)
        print(length)
        cv2.imshow("Hand", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
