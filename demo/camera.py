import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
# VideoCapture()中参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频，如cap = cv2.VideoCapture(“../test.avi”)
    def __del__(self):
        # 关闭摄像头。
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
#       image 是返回的捕获到的帧，如果没有帧被捕获到，则该值为空。
#       success 表示帧捕获是否成功，如果成功，success为True，失败为False。
        image = cv2.flip(image, 1)
        image = cv2.imencode('.jpg', image)[1]     # 按照jpg格式编码
#  cv2.imencode()函数是将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输。
        return image.tobytes()      # return 图片字节码bytes

    def gen(self):
        while True:
            # 相当于一直刷新帧
            frame = self.get_frame()  # frame是图片字节码bytes，故下面的字符串拼接要加b'.....'
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame)
