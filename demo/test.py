# coding=utf-8
import urllib
import urllib.request
import hashlib


def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


statusStr = {
    '0': '短信发送成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '账户已过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词'
}

smsapi = "http://api.smsbao.com/"
# 短信平台账号
user = 'ylnx'
# 短信平台密码
password = md5('2003052288mjp')
# 要发送的短信内容
content = '【宿舍监控系统】已到达就寝时间，请及时熄灯入睡。'
# 要发送短信的手机号码
phone = '18390816537'

data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
send_url = smsapi + 'sms?' + data
response = urllib.request.urlopen(send_url)
the_page = response.read().decode('utf-8')
print(statusStr[the_page])