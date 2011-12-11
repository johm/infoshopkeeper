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
from components.discount import item_discount
import os



class DiscountPopup(wxDialog):
    def __init__(self, parent,discount_amount):
        self.parent=parent
        self.discount_amount=discount_amount
        wxDialog.__init__(self, parent,-1,"Discount")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((250, 150))

        self.static1=wxStaticText(self, -1, "Discount Percentage:",pos=wxPoint(15,15))
        self.discount_field=wxTextCtrl(id=-1,name="discount", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0)
        self.discount_field.SetValue("%.2f" % (discount_amount))
        self.discount_field.SetSelection(-1,-1)
        
        self.b = wxButton(self, -1, "Apply Discount", (15, 80))
        EVT_BUTTON(self, self.b.GetId(), self.ApplyDiscount)
        self.b.SetDefault()

        self.b2 = wxButton(self, -1, "Cancel", (115, 80))
        EVT_BUTTON(self, self.b2.GetId(), self.Cancel)


    def Cancel(self,event):
        self.EndModal(1)

    def ApplyDiscount(self,event):
        self.discount_amount=self.discount_field.GetValue()
        total_so_far=self.parent.orderbox.getTotal()
        self.parent.orderbox.append(item_discount(float(self.discount_amount),total_so_far))
        
        self.EndModal(1)
            
        

