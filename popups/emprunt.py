# Copyright 2006 Guillaume Beaulieu 

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

import types

from wxPython.wx import *
from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin

from components.item_inventoried_merchandise import inventoried_merchandise

from popups.inventoriedmerchandise import InventoriedMerchandisePopup
from objects.kind import Kind
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.emprunt import Emprunt
from objects.member import Member
try:
    from etc import bookStatus 
except:
    bookStatus = false

class EmpruntListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wxDefaultPosition, size=(800,300),
                  style=0):
        wxListCtrl.__init__(self, parent, ID, pos, size, style)
        wxListCtrlAutoWidthMixin.__init__(self)

class CheckEmpruntPopup(wxDialog,wxColumnSorterMixin):
    def GetListCtrl(self):
        return self.stuff.list
    
    def __init__(self,parent):
        self.parent=parent
        wxDialog.__init__(self, parent, -1, "Search emprunts")
        self.SetSize(wxSize(800,600))
        self.browser = 0
        self.stuff = CheckEmpruntPanel(parent=self,
                                is_dialog=1)
        
    def close_the_window(self):
        self.EndModal(1)


class CheckEmpruntPanel(wxPanel,wxColumnSorterMixin):
    
    def GetListCtrl(self):
        return self.list
    
    def __init__(self,parent, is_dialog=0):
        self.parent=parent
        self.is_dialog = is_dialog
        if is_dialog:
            self.main_window = parent.parent
        else:
            self.main_window = parent
        self.browser = 0
        wxPanel.__init__(self, parent)
        tID = wxNewId()

        self.master_sizer=wxBoxSizer(wxVERTICAL)
        self.row_1=wxBoxSizer(wxHORIZONTAL)
        self.row_2=wxBoxSizer(wxHORIZONTAL)
        self.row_3=wxBoxSizer(wxHORIZONTAL)
        self.row_4=wxBoxSizer(wxHORIZONTAL)
        self.row_5=wxBoxSizer(wxHORIZONTAL)

        self.static1=wxStaticText(self, -1, "Book Title:")
        self.static2=wxStaticText(self, -1, "Book Author:")
        self.row_1.Add(self.static1,1,wxEXPAND,2)
        self.row_1.Add(self.static2,1,wxEXPAND,2)
        
        self.title=wxTextCtrl(id=-1,name="book_title", parent=self,  style=0)
        self.author=wxTextCtrl(id=-1,name="book_author", parent=self, style=0)

        self.row_2.Add(self.title,1,wxEXPAND,2)
        self.row_2.Add(self.author,1,wxEXPAND,2)
        
        self.static3=wxStaticText(self, -1, "Borrowers first name:")
        self.static4=wxStaticText(self, -1, "Last name:")
        self.row_3.Add(self.static3,1,wxEXPAND,2)
        self.row_3.Add(self.static4,1,wxEXPAND,2)
        
        self.firstname=wxTextCtrl(id=-1,name="firstname", parent=self,  style=0)
        self.lastname=wxTextCtrl(id=-1,name="lastname", parent=self, style=0)
        self.row_4.Add(self.firstname,1,wxEXPAND|wxALL,5)
        self.row_4.Add(self.lastname,1,wxEXPAND|wxALL,5)
        
        self.b2 = wxButton(self, -1, "Search")
        EVT_BUTTON(self, self.b2.GetId(), self.OnSearch)
        self.b2.SetDefault()
        self.row_5.Add(self.b2,0,wxEXPAND|wxALL,5)
        self.b = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, self.b.GetId(), self.OnCancel)
        self.row_5.Add(self.b,0,wxEXPAND|wxALL,5)
       
        self.master_sizer.Add(self.row_1,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_2,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_3,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_4,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_5,0,wxEXPAND|wxALL,5)
        
        self.list = EmpruntListCtrl(self, tID,
                                 style=wxLC_REPORT | wxSUNKEN_BORDER
                                 | wxLC_EDIT_LABELS
                                 #| wxLC_NO_HEADER
                                 #| wxLC_VRULES | wxLC_HRULES
                                 )
        self.list.InsertColumn(0,"Title")
        self.list.InsertColumn(1,"Author")
        self.list.InsertColumn(2,"First Name")
        self.list.InsertColumn(3,"Last Name")
        self.list.InsertColumn(4,"Date")
        self.list.InsertColumn(5,"id")
        
        self.master_sizer.Add(self.list, flag=wxGROW, proportion=1)

        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)


    def OnSearch(self,event):
        self.list.DeleteAllItems()
        self.authorString=self.author.GetValue()
        self.titleString=self.title.GetValue()
        self.firstnameString=self.firstname.GetStringSelection()
        self.lastnameString=self.lastname.GetStringSelection()
        i = 0
        bookcondition={}
        usercondition={}
        bookcondition["author"]=self.authorString
        bookcondition["title"]=self.titleString
        usercondition["fn"]=self.firstnameString
        usercondition["ln"]=self.lastnameString
            
        for x in Emprunt.select("return_date is null"):
            print x.date
            isGood=1
            item = x.getItem()
            member = x.getBorrower()
            titres = item.title # titres = title in french... 
            title = titres.booktitle
            a = Author.select("title_id=\'%d\'" % titres.id)
            a = list(a)
            print "6..."
            if len(a) > 1 or len(a) == 0:
                print "Shit !"
            author = a[0].authorName
            print author
            if len(usercondition) >= 1:
                if len(usercondition["fn"]) > 0 and not(member.first_name.find(usercondition['fn'])):
                    isGood=0
                else:
                    print "f n matches"
                if len(usercondition["ln"]) > 0 and not(member.last_name.find(usercondition['ln'])):
                    isGood=0
                else:
                    print "l n matches"
            if len(bookcondition) >= 1:
                if len(bookcondition["title"]) > 0 and not(title.find(bookcondition['title'])):
                    isGood=0
                else:
                    print "title matches"
                if len(bookcondition["author"]) > 0 and not(author.find(bookcondition["author"])):
                    isGood=0
                else:
                    print "author matches"
            if isGood == 1:
                self.list.InsertStringItem(i,title)
                self.list.SetStringItem(i,1,author)
                self.list.SetStringItem(i,2,member.first_name)
                self.list.SetStringItem(i,3,member.last_name)
                self.list.SetStringItem(i,4,x.date.isoformat())
                self.list.SetStringItem(i,5, "%d" % x.id)
                self.list.SetItemData(i,i)
                i=i+1
        if i>0:
            for x in range(6):
                self.list.SetColumnWidth(x, wxLIST_AUTOSIZE)
        EVT_LIST_ITEM_ACTIVATED(self,self.list.GetId(), self.onSelectItem)

    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()

    def onSelectItem(self,event):
        currentItem = event.m_itemIndex
        m_item=Emprunt.get(self.getColumnText(currentItem, 5))
        m_item.checkin()
        m_item.item.change_status("BORROWABLE")
        if self.is_dialog:
            self.parent.close_the_window()


        

    def OnCancel(self,event):
        if self.is_dialog:
            self.parent.close_the_window()       
        


    
