# Created by He at 06.01.2021

# Feature: sending of the analytics report by e-mail

# Scenario: gets .pdf from folder and sends it via e-mail

#---------------------------------------------------------

import smtplib
import json
from email.message import EmailMessage
from datetime import datetime

full = True
if full:
    try:
        exec(open("get_basedata.py").read())
        exec(open("eval_data.py").read())
        exec(open("gen_report.py").read())
    except:
        exec(open("eval_data.py").read())
        exec(open("gen_report.py").read())

EMAIL_ADDRESS = 'tobiashein32@gmail.com'
#EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
path_to_json = "./tmp/pass.json"

with open(path_to_json, "r") as handler:
    info = json.load(handler)

password = info["password"]
EMAIL_PASSWORD = password
TODAY = datetime.today()
FILE = 'report_NVIDIA.pdf'

# =============================================================================
# SEND EMAIL FUNCTION
# =============================================================================
def send_email():
    # Change the items with: ######Change Me#######
    mail_user = EMAIL_ADDRESS
    mail_app_password = EMAIL_PASSWORD
    sent_from = mail_user
    # sent_to = [mail_user,'tobias.hein@hotmail.de','t.hein@brenk.com']
    sent_to = ['t.hein@brenk.com']
    sent_subject = "Analytics report {}".format(FILE)
    sent_body = "Hier ist der Report!"

    msg = EmailMessage()
    msg['Subject'] = sent_subject
    msg['From'] = mail_user
    msg['To'] = sent_to
    msg.set_content(sent_body)

    with open(FILE, 'rb') as f:
        data = f.read()
        msg.add_attachment(data, filename=FILE, maintype='application/pdf', subtype='pdf')

    email_text = """\
            From: %s
            To: %s
            Subject: %s
            %s
            """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        # server = smtplib.SMTP_SSL('smtp.live.com', 465, mail_user, timeout=120) #hotmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120) as smtp:
            smtp.login(mail_user, mail_app_password)
            smtp.send_message(msg)
        print(email_text)
        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)


# =============================================================================
# END OF SEND EMAIL FUNCTION
# =============================================================================

send_email()