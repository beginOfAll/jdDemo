from wxpy import *
from threading import Thread
import os
import time
import platform

if 'Linux' in platform.system():
    qrPath = r'/home/qr.png'
else:
    qrPath = r'C:\Wangjz\qr.png'


def qr_success(uuid, status, qrcode):
    if os.path.exists(qrPath):
        os.remove(qrPath)
    with open(qrPath, 'wb') as f:
        f.write(qrcode)


def open_bot():
    bot = Bot(qr_callback=qr_success())
    # wl = list()
    # wl.append(bot.friends().search('王建忠的机器人小号')[0])
    # wl.append(bot.friends().search('王琳')[0])
    tuling = Tuling(api_key='0ff917ee3de947d8a9b9894a0bcaba59')

    @bot.register(msg_types='Text')
    def reply_my_friend(msg):
        if msg.text.startswith('。'):
            res = tuling.reply_text(msg)
            if res.find('图灵机器人') > 0:
                res = '你猜呢~'
            msg.reply_msg(res + '  ->Z!')

    bot.join()


def readQR():
    time.sleep(2)
    png_src = b''
    for i in range(10):
        if os.path.exists(qrPath):
            with open(qrPath, 'rb') as f:
                png_src = f.read()
                break
    return png_src


def wechat():
    if os.path.exists(qrPath):
        os.remove(qrPath)
    t1 = Thread(target=open_bot)
    t1.start()
    return readQR()
