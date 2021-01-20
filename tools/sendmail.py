# -*- coding: utf-8 -*-
# sendmail
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.header import Header

def _sendmail(account, from_name, to, subject, content) -> bool:
    def _format_addr(s):
        name,addr = parseaddr(s)
        return formataddr((Header(name,"utf-8").encode(), addr if isinstance(addr,str) else addr))
    
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = _format_addr("{} <{}>".format(from_name, account["name"]))
    msg["To"] = to
    msg["Subject"] = subject
    
    try:
        em = smtplib.SMTP_SSL(account["smtp_host"], account["smtp_port"])
        em.login(account["name"], account["password"])
        em.sendmail(msg["From"], msg["To"], msg.as_string())
        em.quit()
        print("Success!")
        return True
    except Exception as err:
        print("Failed!\n{}".format(err))
        return False

def sendmail(username: str, password: str, smtp_host: str, smtp_port: int,
    from_name: str, send_to: str, subject: str="主题", content="内容") -> bool:
    account = {}
    account["name"] = username.strip()
    account["password"] = password.strip()
    account["smtp_host"] = smtp_host.strip()
    account["smtp_port"] = smtp_port if re.sub(r"[^\d]", r"", str(smtp_port)) == str(smtp_port) else 0
    
    if account["smtp_port"]==0:
        print("err")
        return False
    else:
        return _sendmail(account, from_name, send_to, subject, content)


if __name__ == "__main__":
    pass
