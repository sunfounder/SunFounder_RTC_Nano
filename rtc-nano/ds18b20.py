from basic import _Basic_class

class DS18B20(_Basic_class):

    _RUNTIME = 1000
    C = 0
    F = 1
    def __init__(self):
        self._ds18b20 = []
        while True:
            for i in range(self._RUNTIME):
                for i in os.listdir('/sys/bus/w1/devices'):
                    if i[:3] == '28-':
                        self._ds18b20[i].append(i)
                self.mount = len(self._ds18b20)
                if self.mount > 0:
                    self._info('DS18B20 founded.\nSlave addresses:')
                    for i in range(self.mount):
                        self._info('%d %s' % (i,self._ds18b20[i]))
                    break
                time.sleep(0.001)
            if self.mount > 0:
                break
            else:
                _debug('Timeout. No devices. Check if DS18B20 is connected.')

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if value not in [0, 1]:
            self._error("unit should be set to DS18B20.C(0) or DS18B20.F(1)")
            raise ValueError("unit should be set to DS18B20.C(0) or DS18B20.F(1)")
        self._unit = value

    def get_temperature(self, index):
        _location = '/sys/bus/w1/devices/%s/w1_slave' % self._ds18b20[index]
        while True:
            for i in range(self._RUNTIME):
                try:
                    _tfile = open(_location)
                    _text = _tfile.read()
                    _tfile.close()
                    _secondline = _text.split("\n")[1]
                    if _secondline == '00 00 00 00 00 00 00 00 00 t=0':
                        _flag = 0
                    else:
                        _flag = 1
                        break
                    time.sleep(0.001)
                except:
                    _flag = 0
            if _flag == 1:
                break
            else:
                print('Timeout. No device. Check if device is connected correctly.')

        _temperaturedata = _secondline.split(" ")[9]
        _temperature = float(_temperaturedata[2:])
        _temperature_c = _temperature / 1000
        if self.unit == self.C:
            return _temperature_c
        if self.unit == self.F:
            _temperature_f = _temperature_c * 9.0 / 5.0 + 32.0
            return _temperature_f

    def get_all(self):
        result = []
        for i in range(self.mount):
            result.append(get_temperature(i))
        return result

    def destroy(self):
        pass
