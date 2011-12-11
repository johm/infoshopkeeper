import sys
import string


from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now

from components import db
import etc

#_connection = db.SQLObjconnect()

class Transaction(SQLObjectWithFormGlue):
	_table = "transactionLog"
	_connection = db.conn() 
	action=StringCol()
	amount=FloatCol()
	date=DateTimeCol(default=now)
	schedule = StringCol()            
	info =StringCol()
	owner =StringCol()
	cashier =StringCol() 

	def object_to_form(self):
		self.extracolumns()
		return SQLObjectWithFormGlue.object_to_form(self)

	def extracolumns(self):
		pass

	def void(self):
		pass

	def get_info(self):
		if 'tostring' in dir(self.info):
			return self.info.tostring()
		else:
			return self.info
