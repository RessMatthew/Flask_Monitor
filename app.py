# session类似于一个字典
import base64
import json
import urllib


from flask import Flask, redirect, url_for, render_template, request, session, Response, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from camera import VideoCamera
from faceRecogniction import recognize

app = Flask(__name__)

#设置SECRET_KEY
app.config['SECRET_KEY'] = "2003052288mjp"

# 设置session的有效期方式2【指session可以往后活多长时间】
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)



# 本地配置
username = 'root'
password = 'xiewantong.123'
ip = 'localhost'
port = '3306'
database = "flask_sql"

sql_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(username, password, ip, port, database)
# 'mysql+pymysql://root:2003052288mjp@localhost:3306/flask_sql'

# 配置数据库的地址
app.config['SQLALCHEMY_DATABASE_URI'] = sql_url

#跟踪数据库的修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # 这一行如果不添加，程序会报警告。
# 创建数据库对象
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(16), primary_key=True,unique=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)
    def model2dict(self):
        return {
            'username' : self.username,
            'password' : self.password,
            'email' : self.email
        }
    def __init__(self, username, password,email):
        self.username = username
        self.email = email
        self.password = password
db.create_all()
# 设置session的存储时间
app.permanent_session_lifetime = timedelta(minutes=1)
app.secret_key = "2003052288mjp"

#user页面
@app.route("/user")
def view_user():
    if "user_status" in session:
        user = session['user']
        return render_template('user.html',
                               username=user['username'],
                               password=user['password'],
                               email=user['email'],
                               passwordrpt=user['password']
                               )
    else:
        return render_template('login.html')
# 登陆页面
@app.route("/login",methods=["POST", "GET"] )
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]
        session["user_status"] = "true"
        # 查询表里面名字等于username的
        user = User.query.filter(User.username == username).first()
        if user.password == password:
            u = user.model2dict();
            session['user'] = u
            return view_user()
        else :
            flash("密码错误，请重新输入")
            return render_template('login.html')
    else:
        if "user_status" in session:
            return render_template('user.html')
        return render_template("login.html")

# 注册页面
@app.route("/register",methods=["POST", "GET"] )
def register():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        email = request.form['email']
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        if password != confirmPassword:
            flash("两次的密码不一致，请重新输入")
            return redirect(url_for("register"))
        else:
            insert = User(username=user,password=password,email=email)
            db.session.add(insert)
            db.session.commit()
            return render_template('user.html')

#天气模块
@app.route('/weather')
def weather():
   wcode = "https://restapi.amap.com/v3/weather/weatherInfo?key=8abaa33f0a92beb622f64bf897f507ec&city=430100"
   ret = json.loads(urllib.request.urlopen(wcode).read().decode("utf8"))

   humidity = ret['lives'][0]['humidity'] + "\r\n"
   temperature = ret['lives'][0]['temperature']

   return render_template('weather.html',humidity=humidity,temperature=temperature)

#用户编辑信息
@app.route('/user_edit',methods = ['POST'])
def user_edit():
    username    = request.form["username"]
    password    = request.form["password"]
    passwordrpt = request.form["passwordrpt"]
    email       = request.form["email"]

    if(passwordrpt != password):
        flash("两次的密码不一致，请重新输入")
        return render_template('user.html')
    else:
        #更新数据库
        user = User.query.filter(User.username==username).update({'password': password,'email':email})
        db.session.commit()
        return render_template('index.html')









@app.route('/')
def index():
    # 如果用户登录了就转到主页面，用户没有登录就转到login页面
    if "user_status" in session:
        return render_template('index.html')
    return render_template('login.html')


@app.route("/put_data",methods = ["GET","POST"])
def face_recognize():
    if request.method == "POST":
        imgData = request.form.get("myimg")
    # 因为imgData是base64的数据，要把它转为ndarray
    # 用face-recognition读取外部图片，读取后的格式就是ndarray
    # 这样先将base64解码，存成一个图片
        img_base64_data = base64.b64decode(imgData)
        with open("D:/face_recognize/pic/user_face.png","wb") as f:
            f.write(img_base64_data)
        user_face = "D:/face_recognize/pic/user_face.png"
        local_face = "D:/face_recognize/pic/local_face.png"
        rec = recognize()
        score = rec.analyse_img(file1 = user_face,file2 = local_face)
        if score>90:
            print("true")
            session["user_status"] = "true"
            return {"result":"true"}
        else:
            print("false")
            return {"result":"false"}

    return render_template("videoCamera.html")

@app.route('/video_feed')
def video_feed():
    camera = VideoCamera()
    return Response(camera.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # sendMessage.sendMES() 发送短信
    app.run(host='0.0.0.0', debug=True, threaded=True)
