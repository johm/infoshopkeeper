

from sqlobject.sqlbuilder import *
 
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from upc import upc2isbn
from infoshopkeeper_config import configuration
import string


class inventoried_merchandise:
    def __init__(self,source,parent=None):
        self.price=0
        self.taxable=1
        self.description=""
        self.distributor=""
        self.status="STOCK"
        self.source=source
        self.id=0
        self.parent=parent

    def set_title_and_copy(self,theBook):
        self.setBook(theBook)
        desc=theBook.title.booktitle
        self.setDescription("%s (%s)" % (desc,theBook.notes))
        self.source=theBook.title.kind.kindName
        self.setPrice(theBook.listprice)
        self.setDistributor(theBook.distributor)



    
    def retrieve(self,number):
        isbn=number
        if len(number)==13:
            isbn=upc2isbn(number)
        books =  Book.select(AND(Book.q.titleID==Title.q.id,Title.q.isbn==isbn,Book.q.status=="STOCK") )
        print books
        if len(list(books))==1:
            theBook = books[0]
            if theBook:
                print theBook
                self.setBook(theBook)
                desc=theBook.title.booktitle
                self.setDescription("%s" % desc)
                self.source=theBook.title.kind.kindName
                self.setPrice(theBook.listprice)
                self.setDistributor(theBook.distributor)
                return 1
        else:
            if len(list(books))>1:
                from popups.browseinventory import BrowseInventoryPopup
                self.browser=BrowseInventoryPopup(self.parent,{"isbn":isbn,"status":"STOCK"})
                self.browser.CenterOnScreen()
                self.browser.ShowModal()
                return -1
            else:
                return 0

    def setBook(self,book):
        self.book=book
	try:
            self.book.extracolumns()
        except:
            pass
        
    def setDescription(self,description):
        self.description=description

    def setDistributor(self,distributor):
        self.distributor=distributor

    def setPrice(self,price):
        self.price=price

    def getName(self):
        return self.source+": "+self.description

    def getPrice(self):
        return self.price

    def canBorrow(self):
        if self.status=="BORROWABLE":
            return True
        else:
            return False

    def getBookColumn(self,column_name):
        return getattr(self.book,string.replace(column_name," ",""))

    def getDescription(self):
        return self.description

    def getDistributor(self):
        return self.distributor


    def finalizeOrder(self,cursor,cashier,paid_how):
        try:
            owner=self.book.owner
        except:
            cfg = configuration()
	    owner = cfg.get("default_owner")
        cursor.execute ("""
        INSERT INTO transactionLog SET
        action = "SALE",
        amount = %s,
        cashier = %s,
        date = NOW(),
        info = %s,
        schedule = %s,
        owner = %s,
	paid_how =%s
        """,(self.price,cashier,"[%s] %s" % (self.getDistributor().encode("ascii", "backslashreplace"),self.getName().encode("ascii", "backslashreplace")),self.price_schedule,owner,paid_how))

        try:
            self.book.sellme() # marks as sold
        except:
            pass

        cursor.close()

        
    
