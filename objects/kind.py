import sys

from sqlobject import *
from components import db
from SQLObjectWithFormGlue import SQLObjectWithFormGlue


class Kind(SQLObjectWithFormGlue):
	_connection = db.conn() 
	kindName=StringCol()




