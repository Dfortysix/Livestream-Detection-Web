from flask import flash,Flask,Response,render_template,session,request,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from hantracking import main
from gesture_volume import gestureVolume
from count_finger import countFinger
from facetracking import faceTracking
from posetracking import poseTracking
from detect_realtime import detectRealTime
from detect_video import detectVideo
from __init__ import  app,db,login_required
from model import User,Post
from datetime import datetime


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


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
        return redirect('/')

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


@app.route('/video')
def video():
    return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
@login_required
def stream():
    return render_template('stream.html')

@app.route('/gesture_volume')
def gvolume():
    return Response(gestureVolume(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_gesturevolume')
@login_required
def stream_gesturevolume():
    return render_template('stream_gestureVolume.html')

@app.route('/count_finger')
def cFinger():
    return Response(countFinger(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_count_finger")
@login_required
def stream_count_finger():
    return render_template('stream_count_finger.html')


@app.route("/face_tracking")
def Ftracking():
    return Response(faceTracking(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_face_tracking")
@login_required
def stream_face_tracking():
    return render_template('stream_face_tracking.html')

@app.route("/pose_tracking")
def Ptracking():
    return Response(poseTracking(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stream_pose_tracking")
@login_required
def stream_pose_tracking():
    return render_template('stream_pose_tracking.html')

@app.route("/detectionr")
def feed_detect_realtime():
    return Response(detectRealTime(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/detection_realtime")
@login_required
def detect_realtime():
    return render_template('detection_realtime.html')

@app.route("/detectionv",methods=['POST','GET'])
def feed_detect_video():
    video = request.files['video']
    video_path = 'static/uploads/' + video.filename
    video.save(video_path)

    return Response(detectVideo(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/detection_video")
@login_required
def detect_video():
    return render_template('detection_video.html')


@app.route('/blog')
def blog_home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog.html',
	posts=posts,)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    return render_template('post.html',
	post=post
	)

@app.route('/add_post')
@login_required
def add_post():
    return render_template('add_post.html')

@app.route('/savepost', methods=['POST'])
def savepost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    cover = request.form['cover']

    post = Post(title=title, subtitle=subtitle, author=author, content=content, cover=cover, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect("/blog")

if __name__ == '__main__':
    app.run(debug=True)
