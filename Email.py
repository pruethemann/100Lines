import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'gatsby87@gmx.ch'
PASSWORD = 'krewella187'

import smtplib

def main():
    # set up the SMTP server
    try:
        s = smtplib.SMTP(host='mail.gmx.net', port=587)
        s.starttls()

        s.login(MY_ADDRESS, PASSWORD)
    except Exception as e:
        print(e)



    # send the message via the server set up earlier.
    msg = 'My first message from Python. Thats creepy'
    s.sendmail(MY_ADDRESS, MY_ADDRESS,  msg)
    print('message sent')

    # Terminate the SMTP session and close the connection
    s.quit()


if __name__ == '__main__':
    main()