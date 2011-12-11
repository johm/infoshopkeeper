# Copyright 2006 John Duda 

# This file is part of Infoshopkeeper.

# Infoshopkeeper is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or any later version.

# Infoshopkeeper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Infoshopkeeper; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

from wxPython.wx import *
import os
from etc import open_cash_drawer
from time import time,asctime,localtime
from components import db

class CashInOutPopup(wxDialog):
    def __init__(self, parent, direction):
        self.parent=parent
	if direction == "out":
	    self.name = "Payout cash"
	else: 
	    self.name = "Pitch in cash"
        self.conn=db.connect()
        wxDialog.__init__(self, parent,-1,self.name)
#        self.SetBackgroundColour("FIREBRICK")

        self.static1=wxStaticText(self, -1, self.name, pos=wxPoint(15,15))
        self.amount=wxTextCtrl(id=-1,name="amount", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)
        
        self.amount.SetValue("%.2f" % 0)
        self.amount.SetSelection(-1,-1)

        self.static2=wxStaticText(self, -1, "For what?",pos=wxPoint(15,70))
        self.description=wxTextCtrl(id=-1,name="description", parent=self, pos=wxPoint(15,95), size=wxSize(200,25), style=0)
        
        
        self.b1 = wxButton(self, -1, self.name, (15, 130))
        EVT_BUTTON(self, self.b1.GetId(), self.doIt)
        self.b1.SetDefault()
        self.b2 = wxButton(self, -1, "Cancel", (140, 130))
        EVT_BUTTON(self, self.b2.GetId(), self.Cancel)


    def Cancel(self,event):
        self.EndModal(1)

    def doIt(self,event):
        description=self.description.GetValue()
        try:
            cash_out = float(self.amount.GetValue())
        except:
            cash_out=0
	if self.name == "Pitch in cash":
	    action = "CASH_ADDED"
	    func = self.parent.cashbox.addAmount
	else:
	    action = "CASH_REMOVED"
	    func = self.parent.cashbox.subtractAmount

        if len(description) > 0:
            func(cash_out)
            cursor=self.conn.cursor()
            cursor.execute ("""
            INSERT INTO transactionLog SET
            action = "%s",
            amount = %s,
            date = NOW(),
            info = %s,
            cashier = %s
            """,(action, cash_out,description,self.parent.cashbox.cashier))

            cursor.close()
            os.system(open_cash_drawer)        
            self.EndModal(1)
        else:
            self.static3=wxStaticText(self, -1, "Cash for what?",pos=wxPoint(15,170))
         
class CashPitchInPopup(CashInOutPopup):
    def __init__(self, parent):
        CashInOutPopup.__init__(self, parent, "in")

class CashPayoutPopup(CashInOutPopup):
    def __init__(self, parent):
        CashInOutPopup.__init__(self, parent, "out")
    	


class CashDepositPopup(wxDialog):
    def __init__(self, parent):
        self.parent=parent
        self.name = "Deposit cash"

        self.conn=db.connect()
        wxDialog.__init__(self, parent,-1,self.name)
        self.static1=wxStaticText(self, -1, self.name, pos=wxPoint(15,15))
        self.amount=wxTextCtrl(id=-1,name="amount", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)
        
        self.amount.SetValue("%.2f" % 0)
        self.amount.SetSelection(-1,-1)
        
        self.b1 = wxButton(self, -1, self.name, (15, 70))
        EVT_BUTTON(self, self.b1.GetId(), self.doIt)
        self.b1.SetDefault()
        self.b2 = wxButton(self, -1, "Cancel", (140, 70))
        EVT_BUTTON(self, self.b2.GetId(), self.Cancel)

    def Cancel(self,event):
        self.EndModal(1)

    def doIt(self,event):
        try:
            cash_out = float(self.amount.GetValue())
        except:
            cash_out=0
        self.parent.cashbox.subtractAmount(cash_out)
        cursor=self.conn.cursor()
        cursor.execute ("""
        INSERT INTO transactionLog SET
          action = 'DEPOSIT',
          amount = %s,
          date = NOW(),
          info = "",
          cashier = %s
          """,(cash_out,self.parent.cashbox.cashier))

        cursor.close()
        os.system(open_cash_drawer)        
        self.EndModal(1)




