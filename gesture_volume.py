import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import handtrackingmodule as htm
from math import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume





vd = cv.VideoCapture(0)
#thiet lap kich thuoc cua camera
vd.set(cv.CAP_PROP_FRAME_WIDTH, 720)
vd.set(cv.CAP_PROP_FRAME_HEIGHT, 640)


detection = htm.HandDetection(detectionCon=0.5)

#dieu khien volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume_range =  volume.GetVolumeRange()
minVol = volume_range[0]
maxVol = volume_range[1]

#





def drawCenter(img,color,trung_diem):
    return cv.circle(img,center=trung_diem,radius=10,color=color,thickness=-1)


def gestureVolume():
    Ptime = 0
    Ctime = 0

    while True:
        isTrue,img = vd.read()
        if not isTrue:
            break
        else:
            img = cv.flip(img,1)
            detection.findHands(img)
            lmList = detection.findPostion(img,draw =False)


            if lmList:
                #print(lmList[4],lmList[8])

                x1,y1 = lmList[4][1],lmList[4][2]
                x2,y2 = lmList[8][1],lmList[8][2]
                trung_diem = ((x1+x2)//2,(y1+y2)//2)

                cv.circle(img,center=(x1,y1),radius=10,color=(255,0,255),thickness=-1)
                cv.circle(img,center=(x2,y2),radius=10,color=(255,0,255),thickness=-1)
                cv.line(img,pt1=(x1,y1),pt2=(x2,y2),color=(255,0,255),thickness=2)
                drawCenter(img,(255,0,255),trung_diem)



                length = dist([x1,y1],[x2,y2])
                vol = np.interp(length,(40,250),(minVol,maxVol))
                vol_thanh = np.interp(length,(40,250),(400,100))
                vol_percent = np.interp(length,(40,250),(0,100))
                volume.SetMasterVolumeLevel(vol, None)
                cv.rectangle(img,(50,int(vol_thanh)),(70,400),color = (0,255,0),thickness=-1)
                cv.putText(img,f"{int(vol_percent)}%",(20,450),fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=1,color = (0,255,0),thickness=2)
                print(length,vol)
                if length <40:
                    drawCenter(img,(0,255,0),trung_diem)


            Ctime = time.time()
            fps = 1/(Ctime-Ptime)
            Ptime = Ctime
            cv.rectangle(img,(50,100),(70,400),color = (0,255,0),thickness=3)
            cv.putText(img,"FPS: "+str(int(fps)),(20,70),fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=2,color = (0,255,0),thickness=2)
            ret, buffer = cv.imencode('.jpg', img)  # Chuyển đổi khung hình thành định dạng JPEG

            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # Trả về

            if cv.waitKey(20) & 0xFF == ord("x"):
                break

    vd.release()
    cv.destroyAllWindows()