import cv2 as cv
import mediapipe as mp
import time


class HandDetection():
    def __init__(self, mode=False, model_complexity=1, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hlm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hlm, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPostion(self, img, draw=True):
        lst = []
        if self.results.multi_hand_landmarks:
            for hlm in self.results.multi_hand_landmarks:
                for (id, lm) in enumerate(hlm.landmark):
                    h, w, c = img.shape
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    lst.append([id, cx, cy])
                    # cv.circle(img,(cx,cy),10,(255,0,255),thickness=-1)

            return lst


def main():
    vd = cv.VideoCapture(0)
    Ptime = 0
    Ctime = 0
    detection = HandDetection()

    while True:
        isTrue, img = vd.read()
        if not isTrue:
            break
        else:
            img = cv.flip(img, 1)
            detection.findHands(img)
            detection.findPostion(img)

            Ctime = time.time()
            fps = 1 / (Ctime - Ptime)
            Ptime = Ctime
            cv.putText(img, str(int(fps)), (20, 70), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 255, 0),
                       thickness=2)


            ret, buffer = cv.imencode('.jpg', img)  # Chuyển đổi khung hình thành định dạng JPEG

            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # Trả về
            if cv.waitKey(20) & 0xFF == ord("x"):
                break

    vd.release()
    cv.destroyAllWindows()




# if __name__ == '__main__':
#     main()