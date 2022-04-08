

import datetime
import re
import sys
import easygui

def pick_date(users_option, d_counter):
    date_attempts = d_counter
    date_match = '^[2][0-1]\d\d[.]([0-1][0-9])[.]([0-3][0-9])$'
    if users_option == True:
        now = datetime.datetime.now()
        picked_date = now.strftime('%Y.%m.%d')
        return picked_date
    else:
        #user_date = input('Enter test date YYYY.MM.DD: ')
        user_date = easygui.enterbox(msg='Enter test date. Format YYYY.MM.DD', title='Date of Test.', strip=True)
        if re.match(date_match, user_date):
            picked_date = user_date
            return picked_date
        if re.match(date_match, user_date) == False and date_attempts < 3:
            picked_date = user_date
            return picked_date
        else:
            easygui.msgbox(msg='Date was not valid. Check date format. Program will terminate after 4 failed attempts.', title='Results', ok_button='Ok')
            #sys.exit()
            return 'None'
            
