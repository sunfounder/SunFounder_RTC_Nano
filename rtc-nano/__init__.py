#!/usr/bin/python

import time
from rtc import RTC
from ds18b20 import DS18B20

def _write_file(filename, str_value):
    fp = open(filename, "w")
    fp.write(str_value)
    fp.close()
    
def _read_file(filename):
    fp = open(filename, "r")
    value = fp.readline()
    fp.close()
    return value

def main():
    global usage_dic, temperature, rtc
    usage_dic = {
        'basic'          :'',
    }
    usage_dic['basic']          = \
          'Usage:\n' \
        + '  rtc-nano [option] [control]\n\n' \
        + 'Options:\n' \
        + '    -s    set date_time\n' \
        + '    -h    help informations (this page)\n' \
        + '    -u    Temperature Unit (F/C)\n'
    temperature = DS18B20()
    rtc = RTC()
    temperature.DEBUG = 'debug'
    rtc.DEBUG = 'debug'

def usage(opt = 'basic'):
    print usage_dic[opt]
    quit()

def check_command():
    option = None
    argv_len = len(sys.argv)

    if argv_len > 2:
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
    print('%s\nTemperature: %s'%(rtc.get_datetime(),ds18b20.get_temperature(0)))

def main():
    main_setup()
    option, control = check_command()

    if option == None:
        print_status()
    elif option == '-h':
        usage()
    elif option == '-s':
        rtc.setup()
    elif option == '-u':
        control = '%s' % control
        control = control.lower()
        if control not in ['c', 'f']:
            usage()
        if control == 'c':
            control = 0
        else control == 'f'
            control = 1
        temperature.unit = control