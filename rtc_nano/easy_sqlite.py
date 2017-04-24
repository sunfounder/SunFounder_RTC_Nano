'''
**********************************************************************
* Filename      : SunFounder_Easy_SQLite
* Description   : Very simple sqlite module
* Author        : Cavon
* E-mail        : service@sunfounder.com
* Website       : www.sunfounder.com
* Update        : Cavon    2016-12-02     V1.1.2
**********************************************************************
'''
import sqlite3
import logging

class DB(object):

    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL
              }

    def __init__(self, db_name, table_name='default_table', debug='critical'):
        self.db_name = db_name
        self.table_name = table_name
        self.logger_setup(debug)
        if not self.is_table_exist():
            self.create_table()

    def logger_setup(self, debug):
        self.logger = logging.getLogger("DB")
        self.logger.setLevel(self.LEVELS[debug])
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s  %(name)s  %(levelname)s  %(message)s")
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self.debug = self.logger.debug
        self.info  = self.logger.info

    def get(self, name, default=None):
        db = sqlite3.connect(self.db_name)
        try:
            self.info('Get value')
            cmd = 'SELECT * FROM %s WHERE name="%s"' % (self.table_name, name)
            self.debug(cmd)
            value = db.execute(cmd)
            value = value.fetchall()
            #print "Value", value
            value = value[0][1]
            self.info(' --Done')
        except Exception, e:
            self.debug(e)
            self.info('read error, use default value')
            value = default
        finally:
            db.close()

        return value

    def set(self, name, value):
        db = sqlite3.connect(self.db_name)
        if self.is_name_exist(name):
            self.info('Value exist, set value')
            cmd = 'UPDATE %s SET value = "%s" WHERE name="%s"' % (self.table_name, value, name)
            self.debug(cmd)
            db.execute(cmd)
            self.info('done')
        else:
            self.info("Value not exist, new value")
            cmd = 'INSERT INTO %s(name, value) VALUES ("%s", "%s")' % (self.table_name, name, value)
            self.debug(cmd)
            db.execute(cmd)
            self.info(' --Done')
        db.commit()
        db.close()

    def remove(self, name):
        db = sqlite3.connect(self.db_name)
        if self.is_name_exist(name):
            self.info('Value exist, removing')
            cmd = 'DELETE from %s WHERE name="%s"' % (self.table_name, name)
            self.debug(cmd)
            db.execute(cmd)
            self.info(' --Done')
            result = True
        else:
            result = False
        db.commit()
        db.close()
        return result

    def delete(self, name):
        self.remove(name)

    def get_all(self):
        dic = {}
        db = sqlite3.connect(self.db_name)
        try:
            cmd = 'SELECT * FROM %s' % (self.table_name)
            value_count = db.execute(cmd)
            value_count = value_count.fetchall()
            for row in value_count:
                dic[row[0]] = int(row[1])
        except Exception, e:
            self.debug(e)
        finally:
            db.close()

        return dic

    def is_table_exist(self):
        db = sqlite3.connect(self.db_name)
        try:
            cmd = 'select * from %s' % (self.table_name)
            value_count = db.execute(cmd)
            result = True
        except:
            result = False
        finally:
            db.close()
            return result

    def create_table(self):
        db = sqlite3.connect(self.db_name)
        try:
            self.info("Creating a Table...")
            cmd = 'create table %s (name varchar(20), value int)' % (self.table_name)
            self.debug(cmd)
            db.execute(cmd)
            self.info(" --Done")
        except:
            self.info("Skip, %s table is already exist." % self.table_name)
        finally:
            db.close()

    def is_name_exist(self, name):
        if self.get(name, default=False):
            return True
        else:
            return False

if __name__ == '__main__':
    db=DB('test.db')

    print 'get value a as default = False'
    a = db.get('a', default=False)
    print 'a = ', a

    print 'get value c as default = False'
    c = db.get('c', default=False)
    print 'c = ', c

    print 'set a to 13'
    db.set('a', 13)
    print 'a set to 13'

    print 'set c to 24'
    db.set('c', 24)
    print 'c set to 24'

    print 'get value a as default = False'
    a = db.get('a', default=False)
    print 'a = ', a

    print 'get value c as default = False'
    c = db.get('c', default=False)
    print 'c = ', c

    print "\nSumary:"
    db.sumary()

    print 'set a to 45'
    db.set('a', 45)
    print 'a set to 45'

    print 'set c to 67'
    db.set('c', 67)
    print 'c set to 67'

    print 'get value a as default = False'
    a = db.get('a', default=False)
    print 'a = ', a

    print 'get value c as default = False'
    c = db.get('c', default=False)
    print 'c = ', c

    print "\nSumary:"
    db.sumary()