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

from objects.kind import Kind

from objects.author import Author
from wxPython.wx import *
from infoshopkeeper_config import configuration
from popups.author import ChooseAuthorsPopup
import urllib
import string
from controls.multiplePrices import multiplePrices
import os

cfg = configuration()
bookStatus = cfg.get("bookStatus")
econoscan=cfg.get('econoscan')


try:
    if os.uname()[0]=="Linux":
        ON_LINUX=True # : )
    else:
    	ON_LINUX=False
except:
    ON_LINUX=False #  :( 


class InventoryPopup(wxDialog):
    def __init__(self,parent):
        self.known_title=False
	self.parent=parent
        self.trailing_two=False
	self.selected_kind = cfg.get("default_kind")
        if isinstance(bookStatus, tuple):
            self.statuses=bookStatus
	else:
	    self.statuses = False
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Merchandise Details")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((400, 570))

        self.master_sizer=wxBoxSizer(wxVERTICAL)

        self.toprow=wxBoxSizer(wxHORIZONTAL)
        self.toprow_col1=wxBoxSizer(wxVERTICAL)
        self.toprow_col2=wxBoxSizer(wxVERTICAL)
        self.static0=wxStaticText(self, -1, "Item ID (UPC or ISBN):")
        self.number=wxTextCtrl(id=-1,name="merchandise_id", parent=self, style=wxTE_PROCESS_ENTER)
        EVT_TEXT(self,self.number.GetId(), self.OnText)
        EVT_TEXT_ENTER(self,self.number.GetId(), self.OnTextEnter)
        if ON_LINUX:
            EVT_CHAR(self.number, self.OnKeyDown)

        self.toprow_col1.Add(self.static0,0,wxEXPAND|wxALL,5)
        self.toprow_col1.Add(self.number,0,wxEXPAND|wxALL,5)
        
        self.static0a=wxStaticText(self, -1, "Quantity:")
        self.quantity=wxTextCtrl(id=-1,name="quantity", parent=self, style=0)
        self.quantity.SetValue("1")

        self.toprow_col2.Add(self.static0a,0,wxEXPAND|wxALL,5)
        self.toprow_col2.Add(self.quantity,0,wxEXPAND|wxALL,5)
        
        self.toprow.Add(self.toprow_col1,0,wxEXPAND|wxALL,5)
        self.toprow.Add(self.toprow_col2,0,wxEXPAND|wxALL,5)

        self.master_sizer.Add(self.toprow,0,wxEXPAND|wxALL,5)
        self.row2=wxBoxSizer(wxHORIZONTAL)
        self.static1=wxStaticText(self, -1, "Title:")
        self.description=wxTextCtrl(id=-1,name="merchandise_description", parent=self, style=0)

        self.row2.Add(self.static1,0,wxGROW,5)
        self.row2.Add(self.description,1,wxGROW,5)
	self.master_sizer.Add(self.row2,0, wxGROW,5)

        self.prices=multiplePrices(self)
        self.prices.addPage(page_name="list price",master=True)
        for m in cfg.get("multiple_prices"):
            self.prices.addPage(page_name=m[0],proportion_of_master=m[1])

        self.prices.render()
        self.master_sizer.Add(self.prices.mp_sizer,1,wxEXPAND|wxALL, 5)
        
        self.row4=wxBoxSizer(wxHORIZONTAL)
        self.static3=wxStaticText(self, -1, "Publisher:")
        self.publisher=wxTextCtrl(id=-1,name="merchandise_publisher", parent=self, style=0)
        self.row4.Add(self.static3,0,wxEXPAND|wxALL,5)
        self.row4.Add(self.publisher,1,wxGROW)
	self.master_sizer.Add(self.row4, 0, wxGROW,5)

        self.row5 = wxBoxSizer(wxHORIZONTAL)
	self.static4=wxStaticText(self, -1, "Author:")
        self.moreAuthor = wxButton(self, -1, "More authors", (110, 500))
        EVT_BUTTON(self, self.moreAuthor.GetId(), self.OnMoreAuthor)
        self.author=wxTextCtrl(id=-1,name="merchandise_author", parent=self, style=0)
	self.row5.Add(self.static4,0,wxEXPAND|wxALL,5)
        self.row5.Add(self.author,1,wxGROW,5,1)
	self.row5.Add(self.moreAuthor,0,wxEXPAND|wxALL,5)
	self.master_sizer.Add(self.row5, 0, wxGROW,5)

	self.row6 = wxBoxSizer(wxHORIZONTAL)
        self.static5=wxStaticText(self, -1, "Category:")
        self.category=wxTextCtrl(id=-1,name="merchandise_category", parent=self, style=0)
        self.row6.Add(self.static5,0,wxEXPAND|wxALL,5)
        self.row6.Add(self.category,1,wxGROW,5,1)
	self.master_sizer.Add(self.row6,0,wxGROW,5)

        self.row7 = wxBoxSizer(wxHORIZONTAL)
	self.static6=wxStaticText(self, -1, "Distributor:")
        self.distributor=wxTextCtrl(id=-1,name="merchandise_distributor", parent=self, style=0)
        self.row7.Add(self.static6,0,wxEXPAND|wxALL,5)
        self.row7.Add(self.distributor,1,wxGROW,5,1)
	self.master_sizer.Add(self.row7, 0, wxEXPAND|wxALL,5)

        self.static7=wxStaticText(self, -1, "Owner:")
        self.owner=wxTextCtrl(id=-1,name="merchandise_owner", parent=self, style=0)
        self.owner.SetValue(cfg.get("default_owner"))
        
        self.master_sizer.Add(self.static7,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.owner,0,wxEXPAND|wxALL,5)

        if self.statuses:
            self.static8=wxStaticText(self, -1, "Status:")
            self.status=wxRadioBox(id=-1,name="Radio box 1", parent=self, choices = self.statuses )

            self.master_sizer.Add(self.static8,0,wxEXPAND|wxALL,5)
            self.master_sizer.Add(self.status,0,wxEXPAND|wxALL,5)


        kinds=["%s" % k.kindName for k in list(Kind.select())]
                
        self.static8=wxStaticText(self, -1, "Kind:")
        self.kind=wxChoice(id=-1,name="merchandise_kind", parent=self,choices=kinds,style=0)

        position = self.kind.FindString(self.selected_kind)
	self.kind.SetSelection(position)

        self.master_sizer.Add(self.static8,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.kind,0,wxEXPAND|wxALL,5)

        self.static9=wxStaticText(self, -1, "Notes:")
        self.notes=wxTextCtrl(id=-1,name="merchandise_notes", parent=self, style=0)
        
        self.master_sizer.Add(self.static9,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.notes,0,wxEXPAND|wxALL,5)

        self.b = wxButton(self, -1, "Add and continue", (15, 500))
        EVT_BUTTON(self, self.b.GetId(), self.OnAddAndContinue)

        self.b2 = wxButton(self, -1, "Add and quit", (110, 500))
        EVT_BUTTON(self, self.b2.GetId(), self.OnAddAndQuit)
        self.b3 = wxButton(self, -1, "Cancel", (110, 500))
        EVT_BUTTON(self, self.b3.GetId(), self.OnCancel)

        self.bottomrow=wxBoxSizer(wxHORIZONTAL)
        self.bottomrow.Add(self.b,1,wxGROW, 5)
        self.bottomrow.Add(self.b2,1,wxGROW, 5)
        self.bottomrow.Add(self.b3,1,wxGROW, 5)
        
        self.master_sizer.Add(self.bottomrow,0,wxEXPAND|wxALL,5)
        self.statusBar = wxStatusBar(self, -1, name="statusBar")
        self.master_sizer.Add(self.statusBar,0,wxEXPAND|wxALL,5)
        
        self.number.SetFocus()  
        self.Fit()
	self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)

    def OnKeyDown(self,event):
        keycode = event.GetKeyCode()
        if event.AltDown() == 1:
            print keycode
            if len(self.number.GetValue())==0:
                self.trailing_two=False
            self.keybuffer= "%s%s" % (self.keybuffer,keycode-48)
            
            if len(self.keybuffer) == 2 and econoscan:
                if len(self.number.GetValue())==12:
                    if self.keybuffer=='05':
                        self.number.SetValue(self.number.GetValue() + "%s" % (2))
                        self.trailing_two=True

            if len(self.keybuffer) == 3:
                keybuffer_as_int= int(self.keybuffer) - 48
                if self.trailing_two:
                    self.number.SetValue(self.number.GetValue()[:-1])
                self.number.SetValue(self.number.GetValue() + "%s" % (keybuffer_as_int))
                if econoscan and keybuffer_as_int==2:
                    self.keybuffer="0"
                else:
                    self.keybuffer=""
                
        else:
            event.Skip()

    def OnMoreAuthor(self, event):
    	win = ChooseAuthorsPopup(self, self.OnGetAuthors)
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()

    def OnGetAuthors(self, authors):
    	authorstring=Author.get(authors.pop(0)).author_name.decode("string_escape")
	for author in authors:
	    # we make a string !
	    authorstring = authorstring + "," + Author.get(author).author_name.decode("string_escape")
	self.author.SetValue(authorstring)

    def OnTextEnter(self,event):
        self.known_title=False
        id=self.number.GetValue()
        
        if (len(id) == 10 or len(id) == 13):
            item=self.parent.inventory.lookup_by_isbn(id)
        else:
            item=self.parent.inventory.lookup_by_upc(id)
      
        if item['known_title']:
            self.known_title=item['known_title']
        
        if item['title']:
            self.number.SetEditable(False)
            self.description.SetValue(item['title'])
            self.prices.pages['list price'].price_ctrl.SetValue("%s" % (item['list_price']))
            self.prices.update_pages(None)
	    self.author.SetValue(item['authors_as_string'])
            self.category.SetValue(item['categories_as_string'])
            self.publisher.SetValue(item['publisher'])
            self.number.SetValue(item['isbn'])

    def OnText(self,event):
        id=self.number.GetValue()
        if len(id) == 13:
		self.OnTextEnter(event)
                

    def OnCancel(self,event):
        self.EndModal(1)

    def OnAddAndContinue(self,event):
    	desc = self.description.GetValue()
	self.AddBook(event)
        self.statusBar.SetStatusText("%s added to book list" % desc)
    
    def OnAddAndQuit(self,event):
        if self.AddBook(event):
	    self.OnCancel(event)
    
    def AddBook(self,event):
        description=self.description.GetValue() 
        try: 
            price_raw=self.prices.pages['list price'].price_ctrl.GetValue()
            price_corrected=string.replace(price_raw,"$","")
            price = float(price_corrected)
        except Exception,e:
            price=0
            
        if len(description) > 0 and price > 0:
            #here we get values and add to inventory
            
            author_as_string=self.author.GetValue()
            authors=string.split(author_as_string,",")
            categories_as_string=self.category.GetValue()
            categories=string.split(categories_as_string,",")
            publisher=self.publisher.GetValue()
            distributor=self.distributor.GetValue()
            owner=self.owner.GetValue()
            notes=self.notes.GetValue()
            isbn=self.number.GetValue()
            quantity=self.quantity.GetValue()
            kind=self.kind.GetStringSelection()
	    if self.statuses:
	        status=self.status.GetSelection()
		writtenStatus = self.statuses[status]
            else: 
	        writtenStatus = ""
            extra_prices={}
            for m in cfg.get("multiple_prices"):
                mprice_raw=(self.prices.pages[m[0]]).price_ctrl.GetValue()
                mprice_corrected=string.replace(mprice_raw,"$","")
                mprice = float(mprice_corrected)
                print "mprice was %s" % mprice
                extra_prices[m[0]]=mprice
            
            self.parent.inventory.addToInventory(title=description,status=writtenStatus,authors=authors,publisher=publisher,price=price,isbn=isbn,categories=categories,distributor=distributor,quantity=quantity,known_title=self.known_title,kind_name=kind,extra_prices=extra_prices,owner=owner,notes=notes)
            
            self.quantity.SetValue("1")
            self.description.SetValue("")
            self.prices.pages['list price'].price_ctrl.SetValue("0.0$")
            self.author.SetValue("")
            self.notes.SetValue("")
            self.category.SetValue("")
            self.publisher.SetValue("")
            self.number.SetValue("")
            self.number.SetFocus()
            self.known_title=False
            self.number.SetEditable(True)
	    return True;
        else:
            dlg = wxMessageDialog(self, "Fill in (at least) title and price correctly !", "Error", wxICON_ERROR|wxOK)
	    dlg.ShowModal()
	    return False;



