# session类似于一个字典

from flask import Flask, redirect, url_for, render_template, request, session, Response, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from camera import VideoCamera


app = Flask(__name__)


# 本地配置
username = 'root'
password = '2003052288mjp'
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
    username = db.Column(db.String(80), primary_key=True,unique=True)
    password = db.Column(db.String(320), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
db.create_all()
# 设置session的存储时间
app.permanent_session_lifetime = timedelta(minutes=1)
app.secret_key = "2003052288mjp"

# 登陆页面
@app.route("/login",methods=["POST", "GET"] )
def login():
    if request.method == "POST":
        username = request.form["userName"]
        password = request.form["passwd"]
        # 查询表里面名字等于username的
        user = User.query.filter(User.username == username).first()
        if user.password == password:
            return render_template("main.html")
        else :
            flash("密码错误，请重新输入")
            return redirect(url_for('login'))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

# 注册页面
@app.route("/register",methods=["POST", "GET"] )
def register():
    if request.method == "POST":
        session.permanent = True
        user = request.form["userName"]
        password = request.form["passwd"]
        session["user"] = user
        session["password"] = password
        inset = User(username=user,password=password)
        db.session.add(inset)
        db.session.commit()
        return redirect(url_for("user"))


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        password = session["password"]
        return f"<h1>{user}{password}</h1>"
    else:
        return redirect(url_for("login"))

@app.route('/')
def index():
    # 如果用户登录了就转到主页面，用户没有登录就转到login页面
    if "user" in session:
        return render_template('index.html')
    return redirect(url_for("login"))



@app.route('/video_feed')
def video_feed():
    camera = VideoCamera()
    return Response(camera.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # sendMessage.sendMES() 发送短信
    app.run(host='0.0.0.0', debug=True, threaded=True)
