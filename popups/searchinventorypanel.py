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
from infoshopkeeper_config import configuration
cfg = configuration()
bookStatus = cfg.get("bookStatus")

class InventoryListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wxDefaultPosition, 
    #size=(800,300),
                  style=0):
        wxListCtrl.__init__(self, parent, ID, pos, 
	#size, 
	style=style)
        wxListCtrlAutoWidthMixin.__init__(self)



class SearchInventoryPanel(wxPanel,wxColumnSorterMixin):
    
    def GetListCtrl(self):
        return self.list
    
    def __init__(self,parent, is_dialog=0):
        self.parent=parent
        self.lastSearchModified = False
        self.is_dialog = is_dialog
        if is_dialog:
            self.main_window = parent.parent
        else:
            self.main_window = parent
        self.browser = 0
        self.selected_kind=cfg.get("default_kind")

        wxPanel.__init__(self, parent)
        tID = wxNewId()

        self.master_sizer=wxBoxSizer(wxVERTICAL)
        self.row_1=wxBoxSizer(wxHORIZONTAL)
        self.row_2=wxBoxSizer(wxHORIZONTAL)
        self.col_3=wxBoxSizer(wxVERTICAL)
        self.row_4=wxBoxSizer(wxHORIZONTAL)
        self.row_5=wxBoxSizer(wxHORIZONTAL)
        self.row_6=wxBoxSizer(wxHORIZONTAL)

        self.static1=wxStaticText(self, -1, "Title:")
        self.static2=wxStaticText(self, -1, "Author:")
        self.static3=wxStaticText(self, -1, "Category:")
        self.row_1.Add(self.static1,1,wxEXPAND,2)
        self.row_1.Add(self.static2,1,wxEXPAND,2)
        self.row_1.Add(self.static3,1,wxEXPAND,2)
        
        self.description=wxTextCtrl(id=-1,name="merchandise_description", parent=self,  style=0)
        self.author=wxTextCtrl(id=-1,name="merchandise_author", parent=self, style=0)
        self.category=wxTextCtrl(id=-1,name="merchandise_category", parent=self, style=0)

        self.row_2.Add(self.description,1,wxEXPAND,2)
        self.row_2.Add(self.author,1,wxEXPAND,2)
        self.row_2.Add(self.category,1,wxEXPAND,2)
        
        self.static5=wxStaticText(self, -1, "Kind:")
        self.col_3.Add(self.static5,1,wxEXPAND,2)
        
        kinds=["%s" % k.kindName for k in list(Kind.select())]
        self.kind=wxChoice(id=-1,name="merchandise_kind", parent=self, choices=kinds)
        self.col_3.Add(self.kind,0,wxGROW)
        if bookStatus:
            self.status=wxRadioBox(id=-1,name="status", label="Status", parent=self, choices = bookStatus ) # bookStatus from etc
        position = self.kind.FindString(self.selected_kind)
        self.kind.SetSelection(position)

        self.row_4.Add(self.col_3,0)
        if bookStatus:
            self.row_4.Add(self.status,0)


        self.b2 = wxButton(self, -1, "Search")
        EVT_BUTTON(self, self.b2.GetId(), self.OnSearch)
        self.b2.SetDefault()
        self.row_4.Add(self.b2,0,wxEXPAND|wxALL,5)

        if self.is_dialog:        
            self.b = wxButton(self, -1, "Cancel")
            EVT_BUTTON(self, self.b.GetId(), self.OnCancel)
            self.row_4.Add(self.b,0,wxEXPAND|wxALL,5)
       
        self.master_sizer.Add(self.row_1,0,wxEXPAND|wxALL)
        self.master_sizer.Add(self.row_2,0,wxEXPAND|wxALL)
        self.master_sizer.Add(self.row_4,0,wxGROW)
        
        self.list = InventoryListCtrl(self, tID,
                                 style=wxLC_REPORT | wxSUNKEN_BORDER
                                 | wxLC_EDIT_LABELS
                                 #| wxLC_NO_HEADER
                                 #| wxLC_VRULES | wxLC_HRULES
                                 )
        self.list.InsertColumn(0,"Title")
        self.list.InsertColumn(1,"Author")
        self.list.InsertColumn(2,"Price")
        self.list.InsertColumn(3,"Publisher")
        self.list.InsertColumn(4,"Status")
        self.list.InsertColumn(5,"ISBN")
        self.list.InsertColumn(6,"Distributor")
        self.list.InsertColumn(7,"Notes")
        self.list.InsertColumn(8,"ID")
        self.list.InsertColumn(9,"Kind")
        
        self.master_sizer.Add(self.list, flag=wxGROW, proportion=1)

        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)


    def OnSearch(self,event):
        self.list.DeleteAllItems()
        self.authorString=self.author.GetValue()
        self.categoryString=self.category.GetValue()
        self.titleString=self.description.GetValue()
        self.kindString=self.kind.GetStringSelection()
        self.lastSearchModified = False
        if self.browser != 0:
            self.browser.EndModal(1)

        
        queryTerms={}
        if bookStatus:
            queryTerms["status"] = bookStatus[self.status.GetSelection()]
        if len(self.authorString) > 0:
            queryTerms["authorName"]=self.authorString
        if len(self.categoryString) > 0:
            queryTerms["categoryName"]=self.categoryString
        if len(self.titleString) > 0:
            queryTerms["title"]=self.titleString
        if len(self.kindString) > 0:
            queryTerms["kind"]=self.kindString
            
        inv=self.main_window.inventory.getInventory(queryTerms)
        self.itemDataMap=inv
        i=0

        items = inv.items()
        for x in range(len(items)):
            key, data = items[x]
            data_3=data[3]
            if not(type(data_3) in types.StringTypes):
                try:
                    data_3=data_3.tostring()
                except AttributeError,TypeError:
                    data_3=""
            data_6=data[6]
            if not(type(data_6) in types.StringTypes):
                try:
                    data_6=data_6.tostring()
                except AttributeError,TypeError:
                    data_6=""

            self.list.InsertStringItem(i,data[0])
            self.list.SetStringItem(i,1,data[1])
            self.list.SetStringItem(i,2,str(data[2]))
            self.list.SetStringItem(i,3,data_3)
            self.list.SetStringItem(i,4,data[4])
            self.list.SetStringItem(i,5,data[5])
            self.list.SetStringItem(i,6,data[6])
            self.list.SetStringItem(i,7,"%s" % (data[7]))
            self.list.SetStringItem(i,8,"%s" % (data[8]))
            self.list.SetStringItem(i,9,"%s" % (data[9]))
            self.list.SetItemData(x,key)
                 
            i=i+1
            
        self.list.SetColumnWidth(0, 200)
        self.list.SetColumnWidth(1, 100)
        self.list.SetColumnWidth(2, 40)
        self.list.SetColumnWidth(5, 35)
        self.list.SetColumnWidth(8, 50)

        wxColumnSorterMixin.__init__(self, 9)
        self.SortListItems(0, True)
        EVT_LIST_ITEM_ACTIVATED(self,self.list.GetId(), self.onSelectItem)

    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()
    
    def removeItem(self,index):
        self.lastSearchModified = True
        self.list.DeleteItem(index)
        return true

    def onSelectItem(self,event):
        currentItem = event.m_itemIndex
        m_item=inventoried_merchandise(self.getColumnText(currentItem, 9))
        m_item.setBook(Book.get(int(self.getColumnText(currentItem, 8))))
        m_item.setPrice(self.getColumnText(currentItem, 2))
        m_item.setDescription(self.list.GetItemText(currentItem))
        m_item.status=self.getColumnText(currentItem,4)
        m_item.database_id=self.getColumnText(currentItem,8) 
        m_item.source=self.getColumnText(currentItem,9) 
        m_item.searchWindowIndex = event.m_itemIndex
        win = InventoriedMerchandisePopup(self.parent,m_item, main_window=self.main_window)

        # Show the popup right below or above the button
        # depending on available screen space...
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        #win.Position(pos, (0, sz.height))
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
            


        

    def OnCancel(self,event):
        if self.is_dialog:
            self.parent.close_the_window()       
        


    

