import smtplib
from email.mime.text import MIMEText


def email(username_recv, content):
    """
    :param username_recv: 用户邮箱
    :param content: 邮件内容
    :return:
    """
    mailserver = "smtp.163.com"
    username_sender = "linyi3537@163.com"
    password = "311219ma"
    username_recv = username_recv
    mail = MIMEText(content)
    mail["Subject"] = "上海票据交易所回复邮件"
    mail["From"] = username_sender  # 发件人
    mail["To"] = username_recv
    smtp = smtplib.SMTP(mailserver, port=25)
    smtp.login(username_sender, password)  # 登录邮箱
    smtp.sendmail(username_sender, username_recv, mail.as_string())
    smtp.quit()  # 发送完毕后退出smtp
    return None