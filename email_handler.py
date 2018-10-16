import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import config


class EmailHandler(object):

    def __init__(self):
        self.sender = 'luojunxi@entermedia.cn'  # todo
        self.subject = u'漫画加载错误日志'
        self.smtpserver = 'hwsmtp.exmail.qq.com'  # 163网易提供给用户的服务器   todo
        self.username = 'luojunxi@entermedia.cn'  # todo 用项目邮箱
        self.password = 'A4208398a'   # todo
        self.target = 'luojunxi@entermedia.cn'  # todo
        self.file = open(config.LOGGING["FILE"], 'rb+')

    def send_email(self):
        try:
            # log类型的附件
            msg = MIMEMultipart()
            log_part = MIMEApplication(self.file.read())
            log_part.add_header('Content-Disposition', 'attachment', filename='load_error.log')
            msg.attach(log_part)
            msg['Subject'] = self.subject
            msg['From'] = self.sender
            msg['To'] = self.target
            smtp = smtplib.SMTP()
            smtp.connect(self.smtpserver)
            smtp.login(self.username, self.password)
            smtp.sendmail(self.sender, self.target, msg.as_string())
            smtp.quit()
            self.file.close()
            return print("邮件发送成功")
        except Exception as e:
            print(e)
            return print("邮件发送失败")
