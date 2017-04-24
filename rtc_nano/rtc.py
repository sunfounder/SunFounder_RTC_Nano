import subprocess, time
from basic import _Basic_class
import os

class RTC(_Basic_class):
    monthname = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun',
                 '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    monthfullname = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June',
                     '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}

    _class_name = 'RTC'
    def __init__(self, log='debug'):
        self.logger_setup()
        self.DEBUG = log

    def confirm_loop(self, word):
        while True:
            check = raw_input('%s (y/n) '%word)
            if check == 'n' or check == 'N':
                return False
            elif check == 'y' or check == 'Y':
                return True
            else:
                print("\nSorry, I don't understand. I'm expecting a \"y\" or an \"n\" here. So try again. ")

    def setup(self):
        if self.is_rtc_avaible:
            print('\nNow the RTC is:')
            print(subprocess.check_output('sudo hwclock -r',shell=True))
            result = self.confirm_loop('Is it right? Do you need to set the clock?')
            if result:
                self.set_datetime()
            else:
                print('OK, we are done here. Installation finished.')

    @property
    def is_rtc_avaible(self):
        status = subprocess.call('sudo hwclock -r > /tmp/1',shell=True)
        if status == 1:
            self._error('RTC is not availble, please the connection')
            return False
        else:
            self._debug('RTC status: OK, raw value: %s'%status)
            return True

    def set_datetime(self):
        print("\nLet's set the date!")
        confirm = None
        while confirm != True:
            flag = 1
            count_d = 0
            while flag == 1:
                while True:
                    try:
                        date = raw_input('\nType in year, month and date in this format: "YYYY/MM/DD": ')
                        year = date.split('/')[0]
                        month = date.split('/')[1]
                        dateofmonth = date.split('/')[2]
                        break
                    except:
                        print('Error. Try again.')
                print('')
                if int(month) in [1, 3, 5, 7, 8, 10, 12]:
                    if 0 < int(dateofmonth) < 32:
                        flag = 0
                    else:
                        print('%s has only 31 days. Made a mistake? Try again.' % self.monthfullname[month])
                elif int(month) in [4, 6, 9, 11]:
                    if 0 < int(dateofmonth) < 31:
                        flag = 0
                    else:
                        print('%s has only 30 days. Made a mistake? Try again.' % self.monthfullname[month])
                elif int(month) == 2:
                    if int(year)%4 == 0:
                        if 0 < int(dateofmonth) < 30:
                            flag = 0
                        else:
                            print('%s in %s has only 29 days. Fabruary has no more than 29 days even in a leap year! Made a mistake? Try again.' % (self.monthfullname[month], year))
                    else:
                        if 0 < int(dateofmonth) < 29:
                            flag = 0
                        elif int(dateofmonth) == 29: 
                            print('Year %s is a leap year, February has only 28 days. Made a mistake? Try again.' % year)
                        else:
                            print("%s in %s has only 28 days. Even a leap year does not have that much days. Made a mistake? Try again." % (self.monthfullname[month], year))
                else:
                    print('How can it be month %s?! There are only 12 months a year %s. Maybe you made a mistake. Keep in mind: first year, then month, and finally date, each seprated by "/". Try again.' % (month, year))
                
                count_d += 1

            if count_d <= 1:
                print('\nGreat! Pretty easy huh?')

            elif count_d <= 2:
                print('Well, we did it. ')
                
            elif count_d > 2:
                print('Finally, we set the date. It took forever. But anyway.', )
                
            confirm = self.confirm_loop('\nYou set the date to: %s.%s, %s\nAre you sure about that?' % (self.monthname[month], dateofmonth, year))

        print("\nNow! Let's set the time!")
        confirm = None
        while confirm != True:
            flag = 1
            count_t = 0
            while flag == 1:
                while True:
                    try:
                        correnttime = raw_input('\nType in the corrent hour, minute and second in "HH:MM:SS" (in 24-hour time):')
                        hour = correnttime.split(':')[0]
                        minute = correnttime.split(':')[1]
                        second = correnttime.split(':')[2]
                        break
                    except:
                        print('Error. Try again.')
                print('')
                if int(hour) <= 24:
                    if int(hour) == 24:
                        hour = 0
                    flag = 0
                elif int(hour) > 24:
                    print('There are only 24 hours a day. Made a mistake? Try again.')

                elif int(minute) < 60:
                    flag = 0
                elif int(minute) >= 60:
                    print('There are only 60 minutes an hour. Made a mistake? Try again.')

                elif int(second) < 60:
                    flag = 0
                elif int(second) >= 60:
                    print('There are only 60 seconds a minute. Made a mistake? If you are sick of this second thing, just type 00, or any number less than 60. Try again.')

                count_t += 1

            if count_t <= 1 and count_d <= 1:
                print('\nBrilliant! Pretty easy huh?')

            elif count_t <= 2:
                print('\nWell, we did it. ')
                
            elif count_t > 2:
                print('\nFinally, we set the date. It took forever. But anyway.',)

            confirm = self.confirm_loop('\nYou\'ve just set the corrent time to: %s:%s:%s\nAre you sure about that?' % (hour, minute, second))
                    
        print("Great! Now I will correct the time for you.")
        
        print('Setting Linux time...')
        datetimesetting = month+dateofmonth+hour+minute+year+'.'+second
        datetimesetting = "sudo date %s"%datetimesetting
        print(subprocess.check_output(datetimesetting,shell=True))
        print('Done! Set Linux time to')
        print(subprocess.check_output('sudo date',shell=True))
        
        print('\nSetting RTC from Linux time...')
        print(subprocess.check_output('sudo sudo hwclock -w',shell=True))
        print('Done! Set clock on RTC to:')
        print(subprocess.check_output('sudo sudo hwclock -r',shell=True))

        print('\n\nOK, we are done here. Thank you for your support.')

    def get_datetime(self):
        if self.is_rtc_avaible:
            _datetime = subprocess.check_output('sudo hwclock -r',shell=True)
            return _datetime.strip()
        
    def get_date(self):
        _datetime = self.get_datetime()
        split_datetime = _datetime.split(' ')
        _date = [split_datetime[0], split_datetime[1], split_datetime[2], split_datetime[3]]
        _blank = ' '
        _date = _blank.join(_date)
        return _date
    
    def get_time(self):
        _time = self.get_datetime().split(' ')[4]
        if self._clockset == HOUR12 :
            _hour = int(_time.split(':')[0])
            if _hour > 11 :
                apm = 'PM'
            else:
                apm = 'AM'
            if _hour > 12 :
                _hour = _hour - 12
            if _hour == 0:
                _hour = 12
            if _hour < 10:
                _hour = '0%d' % _hour
            _time = '%s:%s:%s %s' % (_hour, _time.split(':')[1], _time.split(':')[2], apm)
        return _time
            
    def get_split_datetime(self):
        _datetime = self.get_datetime()
        split_datetime = _datetime.split(' ')
        _date = [split_datetime[0], split_datetime[1], split_datetime[2], split_datetime[3]]
        _time = split_datetime[4]
        if self._clockset == HOUR12 :
            _hour = int(_time.split(':')[0])
            if _hour > 11 :
                apm = 'PM'
            else:
                apm = 'AM'
            if _hour > 12 :
                _hour = _hour - 12
            if _hour == 0:
                _hour = 12
            if _hour < 10:
                _hour = '0%d' % _hour
            _time = '%s:%s:%s %s' % (_hour, _time.split(':')[1], _time.split(':')[2], apm)
        _blank = ' '
        _date = _blank.join(_date)
        return _date, _time
