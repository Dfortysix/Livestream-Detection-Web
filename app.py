from flask import Flask,Response,render_template
import cv2 as cv
from .hantracking import main
from .gesture_volume import gestureVolume
from .count_finger import countFinger
from .facetracking import faceTracking


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('base.html')

@app.route('/video')
def video():
    return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
    return render_template('stream.html')

@app.route('/gesture_volume')
def gvolume():
    return Response(gestureVolume(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_gesturevolume')
def stream_gesturevolume():
    return render_template('stream_gestureVolume.html')

@app.route('/count_finger')
def cFinger():
    return Response(countFinger(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_count_finger")
def stream_count_finger():
    return render_template('stream_count_finger.html')


@app.route("/face_tracking")
def Ftracking():
    return Response(faceTracking(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_face_tracking")
def stream_face_tracking():
    return render_template('stream_face_tracking.html')

if __name__ == '__main__':
    app.run(debug=True)
