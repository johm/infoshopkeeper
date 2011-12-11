from time import time,asctime,localtime
import db


class cashbox:
    def __init__(self):
        self.conn=db.connect()
        self.date= asctime(localtime(time()))
        self.amount=self.getPreviousAmount()
        
    def setCashier(self,cashier):
        self.cashier=cashier

    def getAmount(self):
        return self.amount

    def addAmount(self,more):
        self.setAmount(self.amount+more)

    def subtractAmount(self,less):
        self.setAmount(self.amount-less)

    def setAmount(self,amount):
        self.amount=amount
        cursor=self.conn.cursor()
        cursor.execute ("""
        INSERT INTO cashbox SET
        amount = %s,
        date = NOW()
        """,(amount))
        cursor.close()


    def getPreviousAmount(self):
        #check the db
        cursor=self.conn.cursor()
        cursor.execute("SELECT amount FROM cashbox ORDER BY date desc LIMIT 1")
        row = cursor.fetchone ()
        amount = 0.0
        if row != None:
            amount = row[0]
        cursor.close()
        cursor=self.conn.cursor()
        cursor.execute ("""
        INSERT INTO transactionLog SET
        action = "OPEN_PRECOUNT",
        amount = %s,
        date = NOW()
        """,(amount))
        cursor.close()
        return amount
        

    def setNewAmount(self,amount):

        cursor=self.conn.cursor()
        cursor.execute ("""
             INSERT INTO transactionLog SET
             action = "OPEN_POSTCOUNT",
             amount = %s,
             cashier = %s,
             date = NOW()
        """,(amount,self.cashier))
        cursor.close()
        self.setAmount(amount)
