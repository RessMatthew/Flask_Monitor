from flask import Flask, request, render_template,jsonify

import base64
import face_recognition

import base64
import random
import os
import face_recognize

import pickle

from flask_sqlalchemy import SQLAlchemy

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

class face(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    faceData = db.Column(db.String(3072), unique=True)

    def __init__(self, faceData):
        self.faceData = faceData
db.create_all()



@app.route("/put_data",methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        imgData = request.form.get("myimg")
    # 因为imgData是base64的数据，要把它转为ndarray
    # 用face-recognition读取外部图片，读取后的格式就是ndarray
    # 这样先将base64解码，存成一个图片
        img_base64_data = base64.b64decode(imgData)
        with open("a.png","wb") as f:
            f.write(img_base64_data)
        imgFile = face_recognition.load_image_file("a.png")
        face_code = face_recognition.face_encodings(imgFile)  # 取到了ndarray数据
        # mysql是不能直接存储ndarray数据的,要利用pickle模块
        # pickle模块的dumps方法可以直接把特殊类型的数据转换成python类型
        if face_code!=[]:
            faces_data = pickle.dumps(face_code[0],protocol=-1)
            insert = face(faceData=faces_data)
            db.session.add(insert)
            db.session.commit()
        else:
            return {"result":"请调整拍照姿势，当前上传的数据没有脸"}
    return render_template("videoCamera.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
