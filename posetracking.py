import mediapipe as mp
import cv2 as cv
import time


def poseTracking():
    Ptime = 0
    Ctime = 0
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    vd = cv.VideoCapture(0)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            isTrue, frame = vd.read()

            if not isTrue:
                break
            # Recolor Feed
            frame = cv.flip(frame, 1)
            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            Ctime = time.time()
            fps = 1 / (Ctime - Ptime)
            Ptime = Ctime

            cv.putText(image, str(int(fps)), (20, 70), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 255, 0),
                       thickness=2)
            ret, buffer = cv.imencode('.jpg', image)  # Chuyển đổi khung hình thành định dạng JPEG

            image = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')  # Trả về


            if cv.waitKey(10) & 0xFF == ord('x'):
                break

    vd.release()
    cv.destroyAllWindows()