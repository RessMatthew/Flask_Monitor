# 调用百度API完成人脸识别
import json

import requests
import base64

class recognize:
    def __init__(self):
        self.client_id = 'uL9oD6i1dtIWmnW1FWBiXqLj'  # ak
        self.client_secret = 'hzw6xGQUt1z5xorGszSXgYuQSEI1PgrP'  # sk
    # 获取access_token
    def getAccessToken(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK

        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.client_id + '&client_secret=' + self.client_secret
        response = requests.get(host)
        if response:
            tokenResult = response.json()
            access_token = tokenResult['access_token']
            return access_token
        return ""

    def read_img(self,img1,img2):

        with open(img1,'rb') as f:
            pic1=base64.b64encode(f.read())
        with open(img2,'rb') as f:
            pic2=base64.b64encode(f.read())

        params=json.dumps([
            {"image":str(pic1,"utf-8"),"image_type":'BASE64',"face_type":"LIVE"},
            {"image":str(pic2,"utf-8"),"image_type":'BASE64',"face_type":"IDCARD"}
        ])
        return params

    def analyse_img(self,file1,file2):
        params = self.read_img(file1,file2)
        api="https://aip.baidubce.com/rest/2.0/face/v3/match"+"?access_token="+ self.getAccessToken()
        content=requests.post(api,params).text

        score=eval(content)['result']['score']

        return score
