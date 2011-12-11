from etc import simple_items


class item:
    def __init__(self,id):
        self.id=id
        self.taxable=1
        self.price=simple_items[id][2]
        self.name=simple_items[id][0]   
        self.label=simple_items[id][1]
        self.taxable=True
        try:
            self.taxable=simple_items[id][3]["taxable"]
        except:
            pass
        
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
        info = %s,
	paid_how= %s
        """,(self.price,cashier,self.getName(), paid_how))
        cursor.close()



