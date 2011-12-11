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

class CashPaymentPopup(wxDialog):
    def __init__(self, parent,payment_info):
        self.parent=parent
        self.payment_info=payment_info
        wxDialog.__init__(self, parent,-1,"Cash payment")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((250, 150))

        self.static1=wxStaticText(self, -1, "Cash recieved",pos=wxPoint(15,15))
        self.cash_in=wxTextCtrl(id=-1,name="cash_in", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)
        self.cash_in.SetValue("%.2f" % parent.orderbox.total_with_tax)
        self.cash_in.SetSelection(-1,-1)
        self.cash_in.SetFocus()
        self.b = wxButton(self, -1, "Do the math", (15, 80))
        EVT_BUTTON(self, self.b.GetId(), self.ComputeChange)
        self.b.SetDefault()
    def ComputeChange(self,event):
        order_total=self.parent.orderbox.total_with_tax
        
        try:
            cash_recv = float(self.cash_in.GetValue())
        except:
            cash_recv=0
            
        if cash_recv >= order_total-0.01:  
            change = cash_recv-order_total
            self.parent.display_field.SetValue("Change Due: %.2f" % change)
            self.parent.cashbox.addAmount(order_total)
	    os.system(open_cash_drawer)
            self.parent.do_receiptPopup(event,"cash")
            self.EndModal(1)
            
        else:
            self.static3=wxStaticText(self, -1, "Not enough cash received!!!!",pos=wxPoint(15,110))

