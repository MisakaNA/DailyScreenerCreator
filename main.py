from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import smtplib
import re
import os


def send_by_mail(email_addr_from, password, email_addr_to, file_name, student_name, date):
    try:
        obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        obj.ehlo()
        obj.login(email_addr_from, password)
        message = MIMEMultipart()

        suject = '[Auto Sent Email] Daily screener for %s on %s' % (student_name, date.replace(' ', ''))
        message['Subject'] = Header(suject, 'utf-8')
        message.attach(MIMEText('This is your NYU daily screener...Fuck Login\n', 'plain', 'utf-8'))

        file = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
        file["Content-Type"] = 'application/octet-stream'
        file["Content-Disposition"] = 'attachment; filename="test.html"'
        message.attach(file)

        obj.sendmail(email_addr_from, email_addr_to, message.as_string())
        obj.close()

        print('Email sent')
    except smtplib.SMTPException as e:
        print('Email not send. \n' + str(e))


def modify_screener_html(date, student_name):
    read_file = open('NYU Daily COVID-19 Screener for Campus Access.html', 'rb')
    file_name = '%s-%s-Screener.html' % (student_name, date)
    new_screener = open(file_name, 'wb')

    for line in read_file:
        if re.search(rb'STUDENT_NAME</p>', line):
            line = line.replace(b'STUDENT_NAME', bytes(student_name, encoding='utf-8'))
        if re.search(rb'CURRENT_DATE</p>', line):
            line = line.replace(b'CURRENT_DATE', bytes(date, encoding='utf-8'))
        new_screener.write(line)
    read_file.close()
    new_screener.close()
    return file_name


def main():
    print('Program now running\nPlease make sure you have open the SMTP feature of your sending email account\n')

    student_name = input('Please enter your name: ')
    email_addr_from = input('Please give me the email address you want to send from: ')
    password = input('Please give me the password of this email address to login to SMTP (Not collect for abuse): ')
    email_addr_to = input('Please give me the email address you want to send to: ')

    while True:
        print('Now waiting for next sending time...')
        date = datetime.now()
        time = str(date.hour) + ':' + str(date.minute) + ":" + str(date.second)
        if time == '21:42:0':
            print(time)
            formatted_date = '%d %s %s' % (date.day, date.strftime('%B')[:3], date.year)
            html_file = modify_screener_html(formatted_date, student_name)
            send_by_mail(email_addr_from, password, email_addr_to, html_file, student_name, formatted_date)

            if os.path.exists(html_file):
                os.remove(html_file)


if __name__ == '__main__':
    main()
