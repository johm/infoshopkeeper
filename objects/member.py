import sys
sys.path.append("/home/john/infoshopkeeper/")

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Member(SQLObjectWithFormGlue):
    _connection = db.conn() 
    first_name = StringCol()
    last_name = StringCol()
    e_mail = StringCol()
    phone = StringCol()
    paid = StringCol()
