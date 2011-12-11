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
import string
import tempfile
import datetime

class ReceiptPopup(wxDialog):
    def __init__(self, parent,payment_info):
        self.parent=parent
        self.payment_info=payment_info
        self.parent.orderbox.listctrl.Append(payment_info)
        wxDialog.__init__(self, parent,-1,"Receipt")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((250, 150))

        self.static1=wxStaticText(self, -1, "Print Receipt?",pos=wxPoint(15,15))
    
        self.b = wxButton(self, -1, "Yes", (15, 70))
        EVT_BUTTON(self, self.b.GetId(), self.PrintReceipt)

        self.b2 = wxButton(self, -1, "No", (110, 70))
        EVT_BUTTON(self, self.b2.GetId(), self.OrderFinished)
        self.b2.SetDefault()
        
    def PrintReceipt(self,event):
        import os

        try:
            if os.uname()[0]=="Linux":
                ON_LINUX=True # : )
        except:        
            ON_LINUX=False # :(
                
        if ON_LINUX:
            receiptfile=open(string.replace("/tmp/receipt-%s.txt" % datetime.datetime.today()," ",""),'w')
        else:
            receiptfile=open("C:\\Documents and Settings\\user\\My Documents\\infoshopkeeper\\receipts\\" + string.replace("%s"  % datetime.datetime.today(),":","-") + ".txt",'w')
            
        receipttext=""

        
        receipttext=receipttext+"\n\n\nSale Made at %s" % ("%s" % (datetime.datetime.today()))[0:16] 
        receipttext=receipttext+ "\n\n"

        for i in self.parent.orderbox.items:
            receipttext=receipttext+ i.getName() + string.rjust(" %.2f\n" % i.getPrice(),80-len(i.getName()))

        receipttext=receipttext+"\n"
        
        receipttext=receipttext+ string.rjust("Subtotal:       %.2f\n" % self.parent.orderbox.getTaxableTotal(),80)
        receipttext=receipttext+ string.rjust("Tax:            %.2f\n" % self.parent.orderbox.tax_amount,80)
        receipttext=receipttext+ string.rjust("Total:          %.2f\n" % self.parent.orderbox.total_with_tax,80)
        receipttext=receipttext+ string.rjust("Payment method: %s\n"% self.payment_info,80)

        receiptfile.write(receipttext)
        receiptfile.close()
        self.OrderFinished(event)

    def OrderFinished(self,event):
        #self.parent.orderbox.record_sale()
        self.parent.orderbox.void()
        self.EndModal(1)

