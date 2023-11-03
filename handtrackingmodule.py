import cv2 as cv
import mediapipe as mp
import time



class  HandDetection():
    def __init__(self,mode=False,model_complexity=1,maxHands=2,detectionCon = 0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model_complexity= model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self,img,draw=True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hlm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,hlm,self.mpHands.HAND_CONNECTIONS)

        
        return img 

    def findPostion(self,img,draw=True):
        lst = []
        if self.results.multi_hand_landmarks:
            for hlm in self.results.multi_hand_landmarks:
                for (id, lm) in enumerate(hlm.landmark):
                    h,w,c = img.shape
                    cx = int(lm.x*w)
                    cy = int(lm.y*h)
                    lst.append([id,cx,cy])
                    #cv.circle(img,(cx,cy),10,(255,0,255),thickness=-1)

            return lst
                




