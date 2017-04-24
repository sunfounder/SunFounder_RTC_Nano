#!/usr/bin/python

import time
from rtc import RTC
from ds18b20 import DS18B20
import sys
import easy_sqlite

database_dir = '/var/opt/rtc-nano/rtc-nano.db'
#database_dir = 'rtc-nano.db'

def main_setup():
    global usage_dic, db
    usage_dic = {
        'basic':'',
    }
    usage_dic['basic']          = \
          'Usage:\n' \
        + '  rtc-nano [option] [control]\n\n' \
        + 'Options:\n' \
        + '    -s    set date and time\n' \
        + '    -h    help informations (this page)\n' \
        + '    -u    Temperature Unit (F/C)\n'
    db = easy_sqlite.DB(database_dir)

def usage(opt = 'basic'):
    print usage_dic[opt]
    destroy()

def check_command():
    option = None
    argv_len = len(sys.argv)

    if argv_len > 1:
        option = sys.argv[1]
    else:
        option == None

    if argv_len < 3:
        control = None
    else:
        control = sys.argv[2]

    if argv_len > 4:
        usage()
    return option, control

def print_status():
    temp = DS18B20(log='critical')
    rtc = RTC(log='critical')
    temp.unit = db.get('unit',default='c')
    datetime = rtc.get_datetime()
    temperature = temp.get_temperature(0)
    unit = temp.unit
    print('%s\nTemperature: %s %s'%(datetime,temperature,unit))

def rtc_setup():
    rtc = RTC(log='critical')
    rtc.setup()

def set_unit(value):
    value = '%s' % value
    value = value.lower()
    if value not in ['c', 'f']:
        print "Unit should be C for Celsius, or F for Fahrenheit"
        destroy()
    db.set('unit', value)

def main():
    option, control = check_command()
    main_setup()

    if option == '-h':
        usage()
    elif option == '-s':
        rtc_setup()
    elif option == '-u':
        set_unit(control)
    elif option == None:
        print_status()

def destroy():
    quit()
