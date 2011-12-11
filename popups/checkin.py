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

class CheckinPopup(wxDialog):
    def __init__(self, parent):
        self.parent=parent
        conn=components.db.connect()
        cursor=conn.cursor()
        cursor.execute('select distinct(status) from book where status != "STOCK" and status != "SOLD" order by status')
        self.status_list = [c[0] for c in cursor.fetchall()]
        
        cursor.close()
        
        wxDialog.__init__(self, parent,-1,"Check in items")
        self.SetSize((250, 150))

        self.static1=wxStaticText(self, -1, "Name of Borrower",pos=wxPoint(15,15))
        self.borrower=wxChoice(id=-1,name="Name", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=0,choices=self.status_list)

        self.b = wxButton(self, -1, "Checkin", (15, 80))
        EVT_BUTTON(self, self.b.GetId(), self.Checkin)
        self.b.SetDefault()


    def Checkin(self,event):
        
        status=self.borrower.GetStringSelection()
        books=Book.select(Book.q.status==status)
        frame = wxFrame(None, -1, "check in list" , pos=(50,50), size=(500,600),
                         style=wxNO_FULL_REPAINT_ON_RESIZE|wxDEFAULT_FRAME_STYLE)
        win = CheckinListPopup(frame,books,status)
        #win.Show()

        self.Destroy()
        win.Raise()   
        
        frame.Raise()
        frame.Show()    
        frame.SetFocus()
        




    

class CheckinListPopup(wxScrolledWindow):
    def __init__(self, parent,books,status):
        wxScrolledWindow.__init__(self, parent, -1, wxPoint(0, 0), wxSize(500,600), wxSUNKEN_BORDER)
        self.SetScrollbars(20, 20, 30, 30)
        self.parent=parent
        self.status=status
        self.books=books
        self.master_sizer=wxBoxSizer(wxVERTICAL)

        headers=wxStaticText(self,-1,"Return   Sell   Price",wxPoint(10,10))
        self.master_sizer.Add(headers,0,wxEXPAND|wxALL,3)
        for b in self.books:
            book_element=CheckinListElement(self,b)
            b.element=book_element
            self.master_sizer.Add(book_element,0,wxEXPAND|wxALL,3)

        self.b = wxButton(self, -1, "Checkin")
        self.b.SetForegroundColour("#ff0000")
        EVT_BUTTON(self, self.b.GetId(), self.OnCheckin)
        self.master_sizer.Add(self.b,0,wxEXPAND|wxALL,3)
        
        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)


    def OnCheckin(self,event):
        conn=components.db.connect()
        for b in self.books:
            if b.element.cb_return.GetValue() == True:
                b.change_status("STOCK")
                
            if b.element.cb_sell.GetValue() == True:
                b.sellme()
                cursor=conn.cursor()
                cursor.execute ("""
                INSERT INTO transactionLog SET
                action = "SALE",
                amount = %s,
                cashier = %s,
                date = NOW(),
                info = %s,
                schedule = %s,
                owner = %s,
                """,(float(b.element.sale_price.GetValue()),self.status,"[%s] %s: %s" % (b.distributor,b.title.kind.kindName,b.title.booktitle),"list price",b.owner))
                cursor.close()
        
        self.parent.Destroy()

            
class CheckinListElement(wxSashWindow):
    def __init__(self,parent,book):
        self.parent=parent
        self.book=book
        wxSashWindow.__init__(self,id=-1,parent=parent,size=wxSize(400,40))
        self.cb_return = wxCheckBox(self, -1,   " Return", wxPoint(10, 10), wxSize(20, 20), wxNO_BORDER)
        self.cb_sell = wxCheckBox(self, -1,   " Sell", wxPoint(50, 10), wxSize(20, 20), wxNO_BORDER)
        EVT_CHECKBOX(self, self.cb_return.GetId(),  self.ReturnChecked)
        EVT_CHECKBOX(self, self.cb_sell.GetId(),  self.SellChecked)

        self.sale_price=wxTextCtrl(self,-1,"listprice",size=wxSize(100,30),pos=wxPoint(90,10))
        self.sale_price.SetValue("%s" % book.listprice)
        wxStaticText(self,-1,book.title.booktitle,wxPoint(200,10))


    def ReturnChecked(self,event):
        self.cb_sell.SetValue(False)

    def SellChecked(self,event):
        self.cb_return.SetValue(False)
