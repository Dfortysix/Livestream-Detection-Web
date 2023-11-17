import cv2 as cv
import os

import numpy as np
import time
import handtrackingmodule as htm




def countFinger():
    folderPath = os.path.join(os.path.dirname(__file__), 'static/fingerimages')
    finger_list = os.listdir(folderPath)

    fl = []
    for i in finger_list:
        img = cv.imread(os.path.join(folderPath, i))
        img = cv.resize(img, (200, 200), interpolation=cv.INTER_AREA)
        fl.append(img)

    vd = cv.VideoCapture(0)
    detector = htm.HandDetection()

    finger_tip = [4, 8, 12, 16, 20]

    Ctime = 0
    Ptime = 0
    while True:
        isTrue,img = vd.read()
        if not isTrue:
            break
        else:
            img = cv.flip(img,1)
            detector.findHands(img)
            lmList = detector.findPostion(img,draw=False)




            if lmList :
                lst= []
                for i in range(0,len(finger_tip)):
                    if i == 0:
                        if lmList[5][1] < lmList[9][1]:
                            if lmList[4][1] < lmList[3][1]:
                                lst.append(1)
                            else:
                                lst.append(0)
                        else:
                            if lmList[4][1] < lmList[3][1]:
                                lst.append(0)
                            else:
                                lst.append(1)
                    else:
                        if lmList[finger_tip[i]][2] < lmList[finger_tip[i]-2][2]:
                            lst.append(1)
                        else:
                            lst.append(0)


                print(lst)
                num_finger = lst.count(1)
                cv.putText(img,text=str(num_finger),org= (40,300),fontFace=cv.FONT_HERSHEY_DUPLEX,fontScale=3,color=(255,255,0),thickness=3)
                h,w,c = fl[num_finger].shape
                img[0:h,0:w] = fl[num_finger]

            #set FPS
            Ctime = time.time()
            fps = 1/(Ctime-Ptime)
            Ptime = Ctime
            cv.putText(img,str(int(fps)),(560,70),fontFace=cv.FONT_HERSHEY_SIMPLEX,fontScale=2,color = (0,255,0),thickness=2)
            ret, buffer = cv.imencode('.jpg', img)  # Chuyển đổi khung hình thành định dạng JPEG

            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # Trả về

            if cv.waitKey(20) & 0xFF == ord("x"):
                break;


    vd.release()
    cv.destroyAllWindows()