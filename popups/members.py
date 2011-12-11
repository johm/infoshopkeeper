# Copyright 2006 Guillaume Beaulieu
# but almost everything is cut and pasted from code by john

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

# I've crammed here the code for searchmemberpopup, addmemberpopup,
# addmemberpanel and browsememberpanel. Those panel are distinct since
# they are used in the checkout popup. Panel are at the end, since 
# they have ugly code...

# Members will be used checking out books only to members of a
# library

from wxPython.lib.mixins.listctrl import wxColumnSorterMixin


from objects.member import Member

from wxPython.wx import *
from infoshopkeeper_config import configuration
from components import db
import string

import os


class AddMemberPopup(wxDialog):
    def __init__(self,parent):
        self.parent = parent 
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Add member")
        self.panel = AddMemberPanel(parent=self, main_window=parent)
#        self.SetSize(wxSize(400, 570))

    def OnCancel(self,event):
        self.EndModal(1)

class MembersListCtrl(wxListCtrl):
    def __init__(self, parent, ID, pos=wxDefaultPosition, size=(800,300),
                  style=0):
        wxListCtrl.__init__(self, parent, ID, pos, size, style)


class ShowMembersPopup(wxDialog):
    def __init__(self,parent):
        self.parent = parent 
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Search members")
        self.panel = ShowMembersPanel(parent=self, main_window=parent, motherDialog=self)
#        self.SetSize(wxSize(600, 570))
   

    def OnCancel(self,event):
        self.EndModal(1)

class AddMemberPanel(wxPanel):
    def __init__(self,parent, main_window, on_successful_add=false, cancel=0):
        self.parent = parent
        self.cancel=cancel
        self.on_successful_add=on_successful_add
        self.main_window = main_window
        wxPanel.__init__(self, parent)
        self.master_sizer=wxBoxSizer(wxVERTICAL)

        self.row1=wxBoxSizer(wxHORIZONTAL)
        self.row2=wxBoxSizer(wxHORIZONTAL)
        self.row3=wxBoxSizer(wxHORIZONTAL)
        self.row4=wxBoxSizer(wxHORIZONTAL)
        self.row5=wxBoxSizer(wxHORIZONTAL)
        self.row6=wxBoxSizer(wxHORIZONTAL)
        
        self.static1=wxStaticText(self, -1, "Member first name")
        self.first_name=wxTextCtrl(id=-1,name="first_name", parent=self, style=wxTE_PROCESS_ENTER)
        self.row1.Add(self.static1,0,wxEXPAND|wxALL,5)
        self.row1.Add(self.first_name,1,wxEXPAND,5)
        self.master_sizer.Add(self.row1, 1, flag=wxGROW)
        
        self.static2=wxStaticText(self, -1, "Member last name")
        self.last_name=wxTextCtrl(id=-1,name="last_name", parent=self, style=wxTE_PROCESS_ENTER)
        self.row2.Add(self.static2,0,wxEXPAND|wxALL,5)
        self.row2.Add(self.last_name,1,wxEXPAND,5)
        self.master_sizer.Add(self.row2, 1, flag=wxGROW)
        
        self.static3=wxStaticText(self, -1, "Member e-mail")
        self.e_mail=wxTextCtrl(id=-1,name="e_mail", parent=self, style=wxTE_PROCESS_ENTER)
        self.row3.Add(self.static3,0,wxEXPAND|wxALL,5)
        self.row3.Add(self.e_mail,1,wxEXPAND,5)
        self.master_sizer.Add(self.row3, 1, flag=wxGROW)
        
        self.static4=wxStaticText(self, -1, "Member phone number")
        self.phone=wxTextCtrl(id=-1,name="phone", parent=self, style=wxTE_PROCESS_ENTER)
        self.row4.Add(self.static4,0,wxEXPAND|wxALL,5)
        self.row4.Add(self.phone,1,wxEXPAND,5)
        self.master_sizer.Add(self.row4, 1, flag=wxGROW)
        
        self.static5=wxStaticText(self, -1, "Membership paid:")
        self.paid=wxRadioBox(id=-1,name="Radio box 1", parent=self, choices = ("paid", "not paid"))
        self.row5.Add(self.static5,0,wxEXPAND|wxALL,5)
        self.row5.Add(self.paid,1,wxEXPAND,2)
        self.master_sizer.Add(self.row5, 1, flag=wxGROW)
        
        self.add_member_continue_button = wxButton(self, -1, "Add and continue")
        EVT_BUTTON(self, self.add_member_continue_button.GetId(), self.OnAddContinue)

        self.add_member_quit_button = wxButton(self, -1, "Add and quit")
        EVT_BUTTON(self, self.add_member_quit_button.GetId(), self.OnAddQuit)

        self.cancel = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, self.cancel.GetId(), self.OnCancel)
        self.row6.Add(self.add_member_continue_button, 1, wxGROW, 5)
        self.row6.Add(self.add_member_quit_button, 1, wxGROW, 5)
        self.row6.Add(self.cancel, 1, wxGROW, 5)
        self.master_sizer.Add(self.row6,1,wxEXPAND|wxALL,5)
        
        self.statusBar = wxStatusBar(self, -1, name="statusBar")
        self.master_sizer.Add(self.statusBar,0,wxEXPAND|wxALL)
        self.first_name.SetFocus()  

        self.SetSizer(self.master_sizer)

    def OnCancel(self,event):
        self.parent.OnCancel(event)

    def OnAddContinue(self, event):
        self.Add(event)
        self.statusBar.SetStatusText("%s %s added to members list" % (self.first_name.GetValue(), self.last_name.GetValue()))
    
    def OnAddQuit(self, event):
        while not self.Add(event):
	    True
	self.OnCancel(event)

    def Add(self,event):
    	retval = true;
        first_name = self.first_name.GetValue()
        last_name = self.last_name.GetValue()
        phone = self.phone.GetValue()
        e_mail = self.e_mail.GetValue()
        paid=self.paid.GetSelection()
        if paid == 0:
            paid = true
        else:
            paid = false
        if first_name != "" and last_name != "" and phone != "" and len(phone) >= 7 and e_mail != "":
            try:
                id = self.main_window.membersList.addToMembers(
                                first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                e_mail=e_mail,
                                paid=paid)
            except:   
                self.statusBar.SetStatusText("didn't add stuff, system crashed instead")
		retval = false
		raise 
	    if paid == true:
		cfg = configuration()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute ("""
                INSERT INTO transactionLog SET
                action = "MEMBER ADD",
                amount = %s,
                cashier = %s,
                date = NOW(),
                info = %s,
    	        paid_how= "CASH"
                """, (cfg.get("membershipfees"),self.parent.parent.cashbox.cashier, (first_name + u" " + last_name).encode("ascii", "backslashreplace")))
                self.parent.parent.cashbox.addAmount(cfg.get("membershipfees"))
	        cursor.close()


        else:
            dlg = wxMessageDialog(self, "Fill all fields !!!")
	    dlg.ShowModal()
	    retval = false
	return retval

class ShowMembersPanel(wxPanel):
    def __init__(self,parent, main_window, motherDialog, on_select=None):
        self.parent = parent 
        self.main_window = main_window
        wxPanel.__init__(self, parent)
        self.motherDialog = motherDialog
        self.on_select = on_select
        self.master_sizer=wxBoxSizer(wxVERTICAL)

        self.grid1=wxGridSizer(rows=2, cols=2)
        self.row3=wxBoxSizer(wxHORIZONTAL)
        self.static1=wxStaticText(self, -1, "First Name:")
        self.static2=wxStaticText(self, -1, "Last Name:")
        self.grid1.Add(self.static1,1,wxGROW,2)
        self.grid1.Add(self.static2,1,wxGROW,2)
        self.first_name=wxTextCtrl(id=-1,name="first_name", parent=self,  style=0)
        self.last_name=wxTextCtrl(id=-1,name="last_name", parent=self, style=0)
        self.grid1.Add(self.first_name, 1, wxGROW, 2)
        self.grid1.Add(self.last_name,1, wxGROW,2)
        self.master_sizer.Add(self.grid1,0,wxEXPAND|wxALL,2)
        
        self.search = wxButton(self, -1, "Search")
        EVT_BUTTON(self, self.search.GetId(), self.OnSearch)
        
        self.cancel = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, self.cancel.GetId(), self.OnCancel)

        self.row3.Add(self.search, 2, wxGROW, 2)
        self.row3.Add(self.cancel, 1, wxGROW, 2)
        self.master_sizer.Add(self.row3,0,wxEXPAND|wxALL,3)
        self.list = MembersListCtrl(self, wxNewId(),
                                 style=wxLC_REPORT | wxSUNKEN_BORDER
                                 | wxLC_EDIT_LABELS
                                 )
        num = 0
        for x in ("First name", "Last name", "E-mail", "Phone", "Paid"):
            self.list.InsertColumn(num, x)
            self.list.SetColumnWidth(num, wxLIST_AUTOSIZE_USEHEADER)
            num = num + 1
        self.master_sizer.Add(self.list, flag=wxGROW, proportion=1)
 
        self.first_name.SetFocus()  

        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)


    def OnCancel(self,event):
        # This will work with this panel on the 
        # checkout dialog and on standalone dialog...
        self.motherDialog.OnCancel(event)

    def OnSearch(self,event):
        self.list.DeleteAllItems()
        self.first_nameS=self.first_name.GetValue()
        self.last_nameS=self.last_name.GetValue()
        queryTerms={}

        if len(self.first_nameS) > 0:
            queryTerms["first_name"]=self.first_nameS.encode("ascii", "backslashreplace")
        if len(self.last_nameS) > 0:
            queryTerms["last_name"]=self.last_nameS.encode("ascii", "backslashreplace")
            
        inv=self.main_window.membersList.searchMembers(queryTerms)
        i=0

        for key, value in inv.iteritems():
            self.list.InsertStringItem(i,value[0])
            self.list.SetStringItem(i,1,value[1])
            self.list.SetStringItem(i,2,value[2])
            self.list.SetStringItem(i,3,value[3])
            self.list.SetStringItem(i,4,value[4])
            self.list.SetItemData(i,key)
                 
            i=i+1
        for x in range(4):
            self.list.SetColumnWidth(x, wxLIST_AUTOSIZE)

        EVT_LIST_ITEM_ACTIVATED(self,self.list.GetId(), self.OnSelect)

    def OnSelect(self,event):
        if self.on_select != None:
            self.on_select(event.GetIndex())
