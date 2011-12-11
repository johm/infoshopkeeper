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

from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin
from components.item_inventoried_merchandise import inventoried_merchandise
from popups.inventoriedmerchandise import InventoriedMerchandisePopup

from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category


import types

class InventoryListCtrl(wxListCtrl, wxListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wxDefaultPosition,
                 size=(800,600), style=0):
        wxListCtrl.__init__(self, parent, ID, pos, size, style)
        wxListCtrlAutoWidthMixin.__init__(self)
        

class BrowseInventoryPopup(wxDialog,wxColumnSorterMixin):
    def GetListCtrl(self):
        return self.list

    def __init__(self,parent,queryTerms):
        self.parent=parent
        self.queryTerms=queryTerms
        wxDialog.__init__(self, parent,-1,"Inventory Browser")
        
        self.SetSize((800, 600))
        tID = wxNewId()
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
	
        inv=self.parent.inventory.getInventory(self.queryTerms)
        self.itemDataMap=inv
        i=0

        items = inv.items()
        for x in range(len(items)):
            key, data = items[x]
            data_3=data[3]
            if not(type(data_3) in types.StringTypes):
                data_3=data_3.tostring()

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


    def onSelectItem(self,event):
        currentItem = event.m_itemIndex
        m_item=inventoried_merchandise("book")
        m_item.setBook(Book.get(int(self.getColumnText(currentItem, 8))))
        m_item.setPrice(self.getColumnText(currentItem, 2))
        m_item.setDescription(self.list.GetItemText(currentItem))
        m_item.source=self.getColumnText(currentItem,9)
        
        win = InventoriedMerchandisePopup(self.parent,m_item,self.parent)

        # Show the popup right below or above the button
        # depending on available screen space...
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        #win.Position(pos, (0, sz.height))
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
        


