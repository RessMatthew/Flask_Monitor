from flask import Flask, request, render_template

from faceRecogniction import recognize

import base64


app = Flask(__name__)

@app.route("/put_data",methods = ["GET","POST"])
def hello():
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
        if(score>90):
            print("true")
            return render_template("login.html")
        else:
            print("false")

    return render_template("videoCamera.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
