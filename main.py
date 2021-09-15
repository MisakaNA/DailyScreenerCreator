# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
import smtplib
import re

def send_by_mail():
    obj = smtplib.SMTP('smtp-relay.gmail.com', 25)
    obj.sendmail('sunyumeng420@gmail.com', 's396259218@gmail.com', 'cnm')


def modify_screener_html(date, student_name):
    read_file = open('NYU Daily COVID-19 Screener for Campus Access.html', 'rb')
    new_screener = open('%s-%s-Screener.html' % (student_name, date), 'wb')

    for line in read_file:
        if re.search(rb'STUDENT_NAME</p>', line):
           line = line.replace(b'STUDENT_NAME', bytes(student_name, encoding='utf-8'))
        if re.search(rb'CURRENT_DATE</p>', line):
            line = line.replace(b'CURRENT_DATE', bytes(date, encoding='utf-8'))
        new_screener.write(line)
    read_file.close()
    new_screener.close()

def main():
    date = datetime.now()
    print(date)
    formatted_date = '%d %s %s' % (date.day, date.strftime('%B')[:3], date.year)
    print(formatted_date)
    modify_screener_html(formatted_date, 'Yumeng Sun')
    send_by_mail()

if __name__ == '__main__':
    main()

