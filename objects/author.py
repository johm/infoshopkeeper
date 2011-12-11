import sys


from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class Author(SQLObjectWithFormGlue):
	_connection = db.conn() 
	titles = RelatedJoin('Title')
	author_name = StringCol(length=40, alternateID=True, default="Anonymous")

