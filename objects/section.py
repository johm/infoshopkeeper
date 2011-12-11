import sys
sys.path.append("/home/john/infoshopkeeper/")

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Section(SQLObjectWithFormGlue):
	_connection = db.conn() 
	sectionName=StringCol()
	sectionDescription=StringCol()
	titles = RelatedJoin('Title')
