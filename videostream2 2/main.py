from flask import Flask, render_template, Response, redirect, request, session, url_for, g
from camera import VideoCamera
from camera import staticVideo

app = Flask(__name__, static_folder='static')
app.secret_key = 'secretkey'

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return render_template('video.html')
        return render_template('index.html')
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user    


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/static_video")
def static_video():
    return render_template("static_video.html")

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='isabel', password='password'))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)