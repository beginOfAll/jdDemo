import os
import smtplib
import sched
import time
import datetime
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from envelopes import Envelope


def new_thread_to_send(email_info):
	t = Thread(target=delay_send, args=(email_info,))
	t.start()
	return True


# 定时发送邮件
def delay_send(email_info):
	file_list = [email_info['atta1'], email_info['atta2'], email_info['atta3']]
	today = str(datetime.date.today())
	run_time_datetime = datetime.datetime.strptime((today + ' ' + email_info['send_time'].replace('：', ':')), '%Y-%m-%d %H:%M:%S')
	sec = (run_time_datetime - datetime.datetime.now()).total_seconds()
	if sec > 0:
		time.sleep(sec)
		send(email_info['title'], email_info['body'], file_list, email_info['from'], email_info['to'], email_info['server'], email_info['pwd'], email_info['cc'])


def send(title, body, filePath, fo, to, server, pwd, cc):
	envelope = Envelope(
		from_addr=fo,
		to_addr=to.split(','),
		subject=title,
		text_body=body,
		cc_addr=cc.split(',')
	)
	for i in filePath:
		if i != '':
			envelope.add_attachment(i)
	envelope.send(server, login=fo, password=pwd, tls=True)


# 带附件的邮件(支持群发)
def sendMailWithFile(title, body, filePath, fo, to, server, pwd, cc=None):
	result = False
	if os.path.exists(filePath) and os.path.isfile(filePath):
		msgAtt = MIMEMultipart()
		msgAtt['From'] = fo
		# 构造send用list
		send_use_to = list()
		# to,cc 类型判断
		if isinstance(to, list):
			msgAtt['To'] = ','.join(to)
			send_use_to.extend(to)
		else:
			msgAtt['To'] = to
			send_use_to.append(to)
		if isinstance(cc, list):
			msgAtt['Cc'] = ','.join(cc)
			send_use_to.extend(cc)
		elif isinstance(cc, str):
			msgAtt['Cc'] = cc
			send_use_to.append(cc)
		# 主题
		msgAtt['Subject'] = Header(title, 'utf-8')
		# 正文
		msgAtt.attach(MIMEText(body, 'plain', 'utf-8'))
		# 构造附件
		with open(filePath, 'rb') as f:
			att = MIMEApplication(f.read())
			att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filePath))
			msgAtt.attach(att)
		smtpObj = smtplib.SMTP(server)
		# smtpObj.set_debuglevel(1)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login(fo, pwd)
		smtpObj.sendmail(fo, send_use_to, msgAtt.as_string())
		smtpObj.quit()
		result = True
	else:
		print("file path error")
	return result

# 995190822@qq.com
# tto = ['wangjz_sz@sina.com', ]
# ccc = ['wangjianzhong1993@qq.com', '995190822@qq.com']

# sendMailWithFile('测试', 'hello world', r'C:\Wangjz\wl2.gif', '857599073@qq.com', tto, 'smtp.qq.com', 'pthryeekctpzbdei',cc=ccc)
# send('测试', 'hello world', r'C:\Wangjz\wl2.gif', '857599073@qq.com', tto, 'smtp.qq.com', 'pthryeekctpzbdei', cc=ccc)
