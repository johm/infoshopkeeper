from string import rjust,ljust
from components.item import item
from components import db

from etc import taxrate

class orderbox:
    def __init__(self,listctrl,parent,name,list_position, searchNotAsDialog = False):
        self.parent=parent
        self.searchNotAsDialog = searchNotAsDialog
        self.listctrl=listctrl
        self.items=[]
        self.width = 30
        self.selected = -1
        self.taxed=False
        self.totaled=False
        self.finalized=False
        self.conn=db.connect()
	self.name=name
	self.list_position=list_position

    def isEmpty(self):
        if len(self.items)>=1:
            return False
        else:
            return True
             
        
    def void(self):
        self.selected = -1
        self.taxed=False
        self.totaled=False
        self.finalized=False
        self.listctrl.Clear()
        if self.searchNotAsDialog and self.parent.searchInventory.lastSearchModified:
            # If the last search got removed elements from it
            # we just search again. This is slow and ugly.
            # Someone should implement a cleaner way of
            # transferring items back and forth on the searchList
            # to the order box.
            self.parent.searchInventory.OnSearch(None)
        self.items=[]

    
    def append(self,i):
        self.totaled=False
        self.items.append(i)
        self.listctrl.Append(ljust(i.getName() + " %.2f" % i.getPrice(),self.width))

    def redisplay(self):
	self.totaled=False
	for i in self.items:
	        self.listctrl.Append(ljust(i.getName() + " %.2f" % i.getPrice(),self.width))
    
    def getTotal(self):
        total_amount=0
        for i in self.items:
            if not(isinstance(i,total)):
                   total_amount=total_amount + i.getPrice() 
        return round(total_amount , 2)

    def isAllBorrowable(self):
        """ This checks if all the items in the order can be borrowed"""
        all_borrowable=True
        for i in self.items:
            try:
                if i.canBorrow() == False:
                    all_borrowable = 0
            except:
                # Coffee is not borrowable
                all_borrowable = 0
        return all_borrowable


    def getTaxableTotal(self):
        total_amount=0
        for i in self.items:
            if not(isinstance(i,total)):
                if not(i.taxable==0):
                    total_amount=total_amount + i.getPrice() 
        return total_amount


    def computeTax(self):
        taxable_total_amount=self.getTaxableTotal()
        self.tax_amount=float("%.2f" % (taxable_total_amount*taxrate))

    def finalize_items(self,paid_how):
        if self.finalized == False:
            for item in self.items:
                item.finalizeOrder(self.conn.cursor(),self.parent.cashbox.cashier,paid_how)
            cursor=self.conn.cursor()
            cursor.execute ("""
            INSERT INTO transactionLog SET
            action = "TAX",
            amount = %s,
            cashier = %s,
            date = NOW(),
            info = %s,
	    paid_how = %s
            """,(self.tax_amount,self.parent.cashbox.cashier,"Sales Tax",paid_how))
            cursor.close()

                
        self.finalized=True

    def setBorrowed(self):
        for item in self.items:
            item.book.change_status("BORROWED")
    
    def change_status(self,new_status):
        for item in self.items:
            if hasattr(item,"book"):
                item.book.change_status(new_status)

    def displayFinalTotal(self):
        total_amount=self.getTotal()
        self.computeTax()
        self.total_with_tax=self.tax_amount+total_amount
        self.parent.numberbox.numberdisplay.SetValue("Total: %.2f" % (self.total_with_tax))
        self.totaled=True



        
    def remove_selected(self):
        if not self.taxed and self.selected != -1:
            if not isinstance(self.items[self.selected],tax):
                self.items.pop(self.selected)
                self.listctrl.Delete(self.selected)
                self.selected=-1
        self.totaled=False
        
    def select(self,i):
        self.selected=i




class tax(item):
    def __init__(self,amount):
        self.price=amount
        self.name="------------------------\nSales Tax              "
        self.label=""

    def finalizeOrder(self,cursor,cashier,paid_how):
	pass
        return 0


class total(item):
    def __init__(self,amount):
        self.price=amount
        self.name="------------------------\n        Total"
        self.label=""

    def finalizeOrder(self,a,b,c):
        return 0


        
