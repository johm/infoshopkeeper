
class item_discount:
    def __init__(self,amount,total):
        self.taxable=0
        self.price=round((amount/100)*total*-1,2)
        self.name="%.2f %% Discount" % (amount)
        self.label="Discount"
        
    def getPrice(self):
        return self.price
    
    def getName(self):
        return self.name
    
    def getLabel(self):
        return self.label
    
    def addToOrder(self):
        return 0
        
    def removeFromOrder(self):
        return 0
    
    def finalizeOrder(self,cursor,cashier,paid_how):
        cursor.execute ("""
        INSERT INTO transactionLog SET
        action = "SALE",
        amount = %s,
        cashier = %s,
        date = NOW(),
        info = %s
        """,(self.price,cashier,self.getName()))
        cursor.close()



