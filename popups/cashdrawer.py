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


class CashDrawerPopup(wxDialog):        
    def __init__(self, parent,cashbox):
        self.parent=parent
        self.cashbox=cashbox
        wxDialog.__init__(self, self.parent,-1,"Welcome Happy Worker!")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((700, 500))
        self.static1=wxStaticText(self, -1, "Name of cashier(s)",pos=wxPoint(15,15))
        self.cashier=wxTextCtrl(id=-1,name="cashier", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)
        self.cashier.SetFocus()
        self.cashier.SetInsertionPoint(0)

        self.static2=wxStaticText(self, -1, "Amount in Drawer",pos=wxPoint(15,70))
        self.drawer_amount=wxTextCtrl(id=-1,name="drawer_amount", value="%.2f" % self.cashbox.amount, parent=self, pos=wxPoint(15,110), size=wxSize(200,25), style=0)

        self.b = wxButton(self, -1, "Start shift", (15, 220))
        EVT_BUTTON(self, self.b.GetId(), self.OnLogin)
        self.b.SetDefault()

#    def OnKeyDown(self,event):
#        print event.GetKeyCode()
#        print event.AltDown()
#        event.Skip()
        
    def OnLogin(self,event):
        cashier=self.cashier.GetValue() 
        try:
            drawer_amount = float(self.drawer_amount.GetValue())
        except:
            drawer_amount=0
            
        if len(cashier) > 0 and drawer_amount > 0:
            self.cashbox.setCashier(cashier)
            self.cashbox.setNewAmount(drawer_amount)
            self.EndModal(0)
            self.Close()

            
        else:
            self.static3=wxStaticText(self, -1, "Fill in both fields!!!!",pos=wxPoint(15,170))


