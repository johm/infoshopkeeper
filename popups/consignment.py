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
import components.db
from objects.book import Book
import datetime

class ConsignmentPopup(wxDialog):
    def __init__(self, parent):
        self.parent=parent
        conn=components.db.connect()
        cursor=conn.cursor()
        cursor.execute('select distinct(owner) from book where status = "SOLD" and (consignment_status != "PAID" or consignment_status IS NULL) order by owner')
        self.owner_list = ["%s" % c[0].decode("string_escape") for c in cursor.fetchall()]
        cursor.close()
        
        wxDialog.__init__(self, parent,-1,"Pay consigners for sold items")
        self.SetSize((250, 150))

        self.static1=wxStaticText(self, -1, "Name of Consigner",pos=wxPoint(15,15))
        self.consigner=wxChoice(id=-1,name="Name", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0,choices=self.owner_list)
	self.consigner.SetSelection(len(self.owner_list))
        self.b = wxButton(self, -1, "Mark items as paid", (15, 80))
        EVT_BUTTON(self, self.b.GetId(), self.PayConsigner)
        self.b.SetDefault()


    def PayConsigner(self,event):
        
        owner=self.consigner.GetStringSelection()
	print self.consigner.GetCurrentSelection()
	print self.consigner.GetSelection()
	print self.consigner.GetStringSelection()
        books=Book.select(Book.q.owner==owner)
        frame = wxFrame(None, -1, "check in list" , pos=(50,50), size=(500,600),
                         style=wxNO_FULL_REPAINT_ON_RESIZE|wxDEFAULT_FRAME_STYLE)
        frame.Show(True)
        win = ConsignmentListPopup(frame,books,owner)
        self.Close()




    

class ConsignmentListPopup(wxScrolledWindow):
    def __init__(self, parent,books,owner):
        wxScrolledWindow.__init__(self, parent, -1, wxPoint(0, 0), wxSize(500,600), wxSUNKEN_BORDER)
        self.SetScrollbars(20, 20, 30, 30)
        self.parent=parent
        self.owner=owner
        self.books=books
        self.master_sizer=wxBoxSizer(wxVERTICAL)

        headers=wxStaticText(self,-1,"Repay",wxPoint(10,10))
        self.master_sizer.Add(headers,0,wxEXPAND|wxALL,3)
        for b in self.books:
            book_element=ConsignmentListElement(self,b)
            b.element=book_element
            self.master_sizer.Add(book_element,0,wxEXPAND|wxALL,3)

        self.b = wxButton(self, -1, "Pay consigner for selected items")
        self.b.SetForegroundColour("#ff0000")
        EVT_BUTTON(self, self.b.GetId(), self.OnPayConsigner)
        self.master_sizer.Add(self.b,0,wxEXPAND|wxALL,3)
        
        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)


    def OnPayConsigner(self,event):
        for b in self.books:
            try:
                if b.element.cb_pay.GetValue() == True:
                    b.consignmentStatus="PAID"
            except:
                pass
        self.parent.Destroy()

            
class ConsignmentListElement(wxSashWindow):
    def __init__(self,parent,book):
        self.parent=parent
        self.book=book
        wxSashWindow.__init__(self,id=-1,parent=parent,size=wxSize(400,40))
        if book.consignmentStatus != "PAID" and book.consignmentStatus != "RETURNED":
            self.cb_pay = wxCheckBox(self, -1,   " Pay", wxPoint(10, 10), wxSize(20, 20), wxNO_BORDER)
        else:
            wxStaticText(self,-1,book.consignmentStatus,wxPoint(10,10))

        self.sale_price=wxTextCtrl(self,-1,"listprice",size=wxSize(100,30),pos=wxPoint(90,10))
        self.sale_price.SetValue("%s" % book.listprice)
        wxStaticText(self,-1,book.title.booktitle,wxPoint(200,10))


