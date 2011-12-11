import sys
import string

from objects.title import Title
from objects.tags import Booktag,Tagcategory,Tagable
from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now

from components import db
from infoshopkeeper_config import configuration
cfg = configuration()

#_connection = db.SQLObjconnect()

class Book(SQLObjectWithFormGlue,Tagable):
	_connection = db.conn() 
	listprice=FloatCol()
	wholesale=FloatCol()
	inventoried_when=DateTimeCol(default=now)
	sold_when=DateTimeCol(default=now)  # we ignore this until the status gets set to "SOLD"  
	status = StringCol(default="STOCK")
	consignmentStatus = StringCol()            
	distributor =StringCol()
	owner =StringCol()
	notes =StringCol() 
	tags = MultipleJoin('Booktag')
	title = ForeignKey('Title')
	tagclass=Booktag
	multiplied=False

        def getTitle(self):
                return self.title

	def set_unique_tag(self,category,key,value):
		matching_tags = [t for t in self.tags if t.key==key and t.category.description==category]

		
        def object_to_form(self):
		self.extracolumns()
		return SQLObjectWithFormGlue.object_to_form(self)

	def extracolumns(self):
		if not(self.multiplied):
			for mp in cfg.get("multiple_prices"):
				try:
					self.addColumn(FloatCol(string.replace(mp[0]," ",""),default=0))
				except:
					pass
			self.multiplied=True
	def sellme(self):
		self.status="SOLD"
		self.sold_when=now()

	def change_status(self,new_status):
		self.status=new_status

