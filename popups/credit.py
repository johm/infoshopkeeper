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

class CreditPopup(wxDialog):
    def __init__(self, parent,m_item):
        self.parent=parent
        self.merchandise=m_item
        wxDialog.__init__(self, parent,-1,"Credit Details")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((250, 350))

        self.static1=wxStaticText(self, -1, "Credit Description:",pos=wxPoint(15,15))
        self.description=wxTextCtrl(id=-1,name="credit_description", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)

        self.static2=wxStaticText(self, -1, "Credit Amount:",pos=wxPoint(15,70))
        self.price=wxTextCtrl(id=-1,name="credit_price", parent=self, pos=wxPoint(15,110), size=wxSize(200,25), style=0)

        self.b = wxButton(self, -1, "Cancel", (15, 220))
        EVT_BUTTON(self, self.b.GetId(), self.OnCancel)

        self.b2 = wxButton(self, -1, "Add to Order", (110, 220))
        EVT_BUTTON(self, self.b2.GetId(), self.OnAdd)
        self.b2.SetDefault()

        

    def OnCancel(self,event):
        self.EndModal(1)

    def OnAdd(self,event):
        description=self.description.GetValue() 
        try:
            price = float(self.price.GetValue())
        except:
            price=0
            
        if len(description) > 0 and price != 0:
            self.merchandise.setDescription(description)
            self.merchandise.setPrice(-1*price)
            
            self.parent.orderbox.append(self.merchandise)
            self.EndModal(1)
            
        else:
            self.static3=wxStaticText(self, -1, "Fill in both fields!!!!",pos=wxPoint(15,170))
