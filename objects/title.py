import sys
import string
import sets
import datetime

from sqlobject import *
from components import db
from objects.tags import Titletag,Tagcategory,Tagable
from SQLObjectWithFormGlue import SQLObjectWithFormGlue

#_connection = db.SQLObjconnect()

class dummybook:
	def __init__(self):
		self.sold_when="-"
		self.dummy=True


class Title(SQLObjectWithFormGlue,Tagable):
	class sqlmeta:
  	    fromDatabase = True
	_connection = db.conn()
	books = MultipleJoin('Book')
	author = RelatedJoin('Author')
	tags= MultipleJoin('Titletag')
	categorys = MultipleJoin('Category')
	sections = RelatedJoin('Section')
	kind = ForeignKey('Kind')
	listTheseKeys=('kind')
	tagclass=Titletag
	
	def copies_in_status(self,status):
		i=0
		for b in self.books:
			if b.status==status:
				i=i+1
		return i

	def authors_as_string(self):
		return string.join ([a.author_name for a in self.author],",")

	def categories_as_string(self):
		return string.join ([c.categoryName for c in self.categorys],",")

	def distributors(self):
		return list(sets.Set([b.distributor for b in self.books]))

	def distributors_as_string(self):
		distributors=self.distributors()
		if distributors is not None:
			distributors=[d for d in distributors if d is not None]
			return string.join(distributors,", ")
		else:
			return ""

	
	def last_book_inventoried(self):
		last_book=dummybook()
		for b in self.books:
			b.dummy=False
			if last_book.dummy==False:
				if b.inventoried_when > last_book.inventoried_when:
					last_book=b
			else:
				last_book=b
		return last_book
	

	
	def first_book_inventoried(self):
		first_book=dummybook()
		for b in self.books:
			b.dummy=False
			if first_book.dummy==False:
				if b.inventoried_when < first_book.inventoried_when:
					first_book=b
			else:
				first_book=b
		return first_book

	def highest_price_book(self):
		high_book=dummybook()
		for b in self.books:
			b.dummy=False
			
			if high_book.dummy==False:
				if b.listprice > high_book.listprice:
					high_book=b
			else:
				high_book=b
		return high_book


		
	def last_book_sold(self):
		last_book=dummybook()
		for b in self.books:
			b.dummy=False
			if b.status=="SOLD":
				if last_book.dummy==False:
					if b.sold_when > last_book.sold_when:
						last_book=b
				else:
					last_book=b
		return last_book

	def first_book_sold(self):
		first_book=dummybook()
		for b in self.books:
			b.dummy=False
			if b.status=="SOLD":
				if first_book.dummy==False:
					if b.sold_when < first_book.sold_when:
						first_book=b
				else:
					first_book=b
		return first_book


