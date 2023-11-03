from flask import flash,Flask,Response,render_template,session,request,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .hantracking import main
from .gesture_volume import gestureVolume
from .count_finger import countFinger
from .facetracking import faceTracking
from .posetracking import poseTracking
from .__init__ import  app,db
from .model import User
import cv2 as cv


@app.route('/')
def hello_world():  # put application's code here
    return render_template('base.html')


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    session.clear()

    if request.method == "POST":

        user_name = request.form.get("user")
        password = request.form.get("password")

        # query user data by the given username
        user = User.query.filter_by(name=user_name).first()


        if not user or not check_password_hash(user.password, password):
            flash("user username not match or wrong password!")
            print("That bai")
            return redirect("/")

        session['user_id'] = user.id
        session['user_name'] = user.name

        flash("Login succesful!")
        print("Thanh cong")
        return redirect('/stream')

    else:

        return render_template("user_login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Loged out!")

    return redirect("/")


# This will be turned off from the html layout and navbar
@app.route("/user_register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":

        user_name = request.form.get("user")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("first password and confirm password not matching!")
            return render_template("user_register.html")

        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        user = User(
            name=user_name,
            password=password_hash,
        )
        db.session.add(user)
        db.session.commit()

        return redirect("/user_login")

    return render_template("/user_register.html")
@app.route('/turn_off_camera')
def turn_off_camera():
    # Tạo một đối tượng VideoCapture để kết nối với camera
    cap = cv.VideoCapture(0)

    # Kiểm tra xem camera có được mở thành công hay không
    if not cap.isOpened():
        return 'Không thể mở camera'

    # Tắt camera
    cap.release()

    return 'Camera đã được tắt'



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

@app.route("/pose_tracking")
def Ptracking():
    return Response(poseTracking(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_pose_tracking")
def stream_pose_tracking():
    return render_template('stream_pose_tracking.html')

if __name__ == '__main__':
    app.run(debug=True)
