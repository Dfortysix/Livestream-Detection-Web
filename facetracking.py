import mediapipe as mp
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

vd = cv.VideoCapture(0)
# Initiate holistic model
def faceTracking():
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            isTrue, frame = vd.read()

            if not isTrue:
                break
            # Recolor Feed
            frame= cv.flip(frame, 1)
            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            # print(results.face_landmarks)

            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

            # Recolor image back to BGR for rendering
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)
                                      )

            ret, buffer = cv.imencode('.jpg', image)  # Chuyển đổi khung hình thành định dạng JPEG

            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # Trả về
            cv.imshow('Raw Webcam Feed', image)

            if cv.waitKey(10) & 0xFF == ord('x'):
                break

    vd.release()
    cv.destroyAllWindows()