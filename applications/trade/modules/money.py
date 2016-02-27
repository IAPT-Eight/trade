#coding: utf-8
import re

def is_valid_money(st):
    money = re.compile('|'.join([
        r'^[£]?(\d*)\.(\d{1,2})$',  # e.g., £.50, .50, £1.50, £.5, .5
        r'^[£]?(\d+)[\.]?$',        # e.g., £500, £5, 500, 5, £5., 5.
    ]))

    money_match = money.match(st)
    return not (money_match == None)
