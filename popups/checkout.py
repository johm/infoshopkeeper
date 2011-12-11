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
import datetime
from objects.emprunt import Emprunt
from popups.members import AddMemberPanel, ShowMembersPanel
class CheckoutPopup(wxDialog):
    def __init__(self, parent):
        self.parent=parent
                
        wxDialog.__init__(self, parent,-1,"Check out items")
        self.mastersizer = wxBoxSizer(wxVERTICAL)
        self.static1 = wxStaticText(self, -1, "Check out to :") 
        self.mastersizer.Add(self.static1)
        self.notebook = wxNotebook(self, -1, style=wxNB_TOP)
        self.new_member_panel = AddMemberPanel(parent=self.notebook, main_window=parent, 
                        on_successful_add=self.Borrow, cancel=self.Close)
        self.notebook.AddPage(self.new_member_panel, "New member")
        self.show_member_panel = ShowMembersPanel(parent=self.notebook, main_window=parent, motherDialog=self, on_select=self.Borrow)
        self.notebook.AddPage(self.show_member_panel, "Existing member")
        self.mastersizer.Add(self.notebook)
        self.SetSizer(self.mastersizer)
        for i in self.parent.orderbox.items:
            print i.database_id, "... ", i.id
        #self.b = wxButton(self, -1, "Checkout", (15, 80))
        #EVT_BUTTON(self, self.b.GetId(), self.Checkout)
        #self.b.SetDefault()
        self.mastersizer.SetSizeHints(self)

    def Borrow(self, id):
        borrower = self.parent.membersList.get(id)
        print borrower
        for i in self.parent.orderbox.items:
            # Check if this work on sqlobject 0.7... I got
            # lots of problem on 0.6.1, and itemID __isn't__
            # defined in emprunt, which is plain weirdness
            e = Emprunt(borrower = id, itemID=i.database_id)
            print i.database_id
        self.parent.orderbox.setBorrowed() 
        self.parent.orderbox.void()
        self.Close()
    
    def OnCancel(self,event):
        self.EndModal(1)
        
    def Checkout(self,event):
        borrower=self.borrower.GetValue()
        if len(borrower)>0:
            today="%s" % datetime.date.today()
            self.parent.orderbox.change_status(today+"-"+borrower)
            self.parent.orderbox.void()
        self.Close()
