# emprunt is a french noun for the transaction of
# "borrowing", I translate.google down to loan, 
# but loan is specific for money... don't you borrow
# anything else than money in USA ? 

# If you find a correct translation, correct this...

import sys
import string


from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now
from objects.book import Book
from objects.member import Member
from components import db
import etc

#_connection = db.SQLObjconnect()

class Emprunt(SQLObjectWithFormGlue):
	_connection = db.conn() 
        borrower=ForeignKey("Member")
        item=ForeignKey("Book")
	return_date=DateTimeCol(default = None)
	date=DateTimeCol(default=now)

        def object_to_form(self):
		self.extracolumns()
       		return SQLObjectWithFormGlue.object_to_form(self)
        def checkin(self):
                self.return_date = now()
                return 1

        def getBorrower(self):
                return self.borrower
        
        def getItem(self):
                return self.item

        def getItemTitle(self):
                return self.item.getTitle()

        def extracolumns(self):
		pass

	def void(self):
		pass

	def get_info(self):
		if 'tostring' in dir(self.info):
			return self.info.tostring()
		else:
			return self.info
