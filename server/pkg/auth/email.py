import yagmail as ym
from config.email import *


def send_email(email, category, data):
    if category == "send-code":
        code = data.get("code")
        yag = ym.SMTP(user=SMTP_USER, password=SMTP_PASSWORD, host=SMTP_HOST)
        contents = [
            f"<h3>{email}您好，</h3>",
            "我们收到您要申请一次性验证码来注册Audio_Classifier应用。",
            f"您的一次性验证码为：{code}",
            "若您并未要求此代码，可以安全地忽略此电子邮件。可能有人误输入了您的电子邮件地址。",
            "<hr/>",
            "来自Audio_Classifier客户端"
        ]
        yag.send(to=email, subject="您的一次性验证码", contents=contents)
