import sys
sys.path.append("/home/john/infoshopkeeper/")

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Category(SQLObjectWithFormGlue):
	_connection = db.conn() 
	title = ForeignKey('Title')
	categoryName = StringCol()
