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
from infoshopkeeper_config import configuration
from controls.multiplePricesNotebook import multiplePricesNotebook
import os

cfg = configuration()

try:
    if os.uname()[0]=="Linux":
        ON_LINUX=True # : )
except:
    ON_LINUX=False #  :(
    
econoscan=cfg.get('econoscan')
    
        
        


    
class InventoriedMerchandisePopup(wxDialog):
    def __init__(self, parent,m_item,main_window):
        self.parent=parent
        self.main_window=main_window
        self.merchandise=m_item
        self.trailing_two=False
        if parent == main_window:
            self.notFromADialog = True
        else:
            self.notFromADialog = False
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Merchandise Details")
        self.SetSize((350, 350))

        self.static0=wxStaticText(self, -1, "Item ID (UPC or ISBN):",pos=wxPoint(15,15))
        self.number=wxTextCtrl(id=-1,name="merchandise_id", parent=self, pos=wxPoint(15,40), size=wxSize(200,25), style=wxTE_PROCESS_ENTER)
        self.number.SetFocus()
        EVT_TEXT(self,self.number.GetId(), self.OnText)
        EVT_TEXT_ENTER(self,self.number.GetId(), self.OnTextEnter)
        if ON_LINUX:
            EVT_CHAR(self.number, self.OnKeyDown)

        self.static1=wxStaticText(self, -1, "Item Description:",pos=wxPoint(15,85))


        self.description=wxTextCtrl(id=-1,name="merchandise_description", parent=self, value=self.merchandise.getDescription(),  pos=wxPoint(15,110), size=wxSize(200,25), style=0)


        self.prices=multiplePricesNotebook(id=-1, name="Prices:",parent=self,pos=wxPoint(15,155),size=wxSize(200,65))
        self.prices.addPage(page_name="list price",master=False) # don't slavemps together here
        self.prices.pages["list price"].SetValue("%s" % (self.merchandise.getPrice()))
        for m in cfg.get("multiple_prices"):
            self.prices.addPage(page_name=m[0],proportion_of_master=m[1])
            if hasattr(self.merchandise,"book"):
                self.prices.pages[m[0]].SetValue("%s" % (self.merchandise.getBookColumn(m[0])))
        


#        self.static2=wxStaticText(self, -1, "Item Price:",pos=wxPoint(15,155))
#        self.price=wxTextCtrl(id=-1,name="merchandise_price", parent=self, pos=wxPoint(15,180),value="%s" % (self.merchandise.getPrice()), size=wxSize(200,25), style=0)


        self.goinv = wxButton(self, -1, "Select from inventory", (15, 230))
        EVT_BUTTON(self, self.goinv.GetId(), self.doInv)

        
        self.b = wxButton(self, -1, "Cancel", (15, 260))
        EVT_BUTTON(self, self.b.GetId(), self.OnCancel)

        self.b2 = wxButton(self, -1, "Add to Order", (110, 260))
        EVT_BUTTON(self, self.b2.GetId(), self.OnAdd)

        if self.merchandise.getDescription() == "":
            self.goinv.SetDefault()
        else:
            self.b2.SetDefault()

        
    def OnKeyDown(self,event):
        keycode = event.GetKeyCode()
        if event.AltDown() == 1:
            if len(self.number.GetValue())==0:
                self.trailing_two=False
            
            print keycode
            self.keybuffer= "%s%s" % (self.keybuffer,keycode-48)
            if len(self.keybuffer) == 2 and econoscan:
                print "HERE1"
                if len(self.number.GetValue())==12:
                    print "HERE2"
                    if self.keybuffer=='05':
                        print "HERE3"
                        self.number.SetValue(self.number.GetValue() + "%s" % (2))
                        self.trailing_two=True

            
            if len(self.keybuffer) == 3:
                keybuffer_as_int= int(self.keybuffer) - 48


                if self.trailing_two:
                    print "HERE!"
                    self.number.SetValue(self.number.GetValue()[:-1])

                self.number.SetValue(self.number.GetValue() + "%s" % (keybuffer_as_int))
                if econoscan and keybuffer_as_int==2:
                    self.keybuffer="0"
                else:
                    self.keybuffer=""
        else:
            event.Skip()


    def OnTextEnter(self,event):
        id=self.number.GetValue()
        result=self.merchandise.retrieve(id)
        if result==1:
            self.number.SetEditable(False)
            self.description.SetValue(self.merchandise.getDescription())
            self.prices.pages["list price"].SetValue("%s" % (self.merchandise.getPrice()))
            for m in cfg.get("multiple_prices"):
                if hasattr(self.merchandise,"book"):
                    self.prices.pages[m[0]].SetValue("%s" % (self.merchandise.getBookColumn(m[0])))
        else:
            if result==-1:
                self.Close()

    def OnText(self,event):
        id=self.number.GetValue()
        if len(id) == 13 or len(id) == 18:
            # we have a upc
            result=self.merchandise.retrieve(id)
            if result==1: 
                self.description.SetValue(self.merchandise.getDescription())
                self.price.SetValue(self.merchandise.getPrice())
            else:
                if result==-1:
                    self.Close()

    def doInv(self,event):
        from popups.searchinventory import SearchInventoryPopup
        win = SearchInventoryPopup(self.parent)
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()



    def OnCancel(self,event):
        self.EndModal(1)

    def OnAdd(self,event):
        description=self.description.GetValue() 
        current_page=self.prices.GetPage(self.prices.GetSelection())
        self.merchandise.price_schedule=current_page.GetName()
        try:
            price= float(current_page.GetValue())
        except:
            price=0
            
        if len(description) > 0 and price > 0:
            self.merchandise.setDescription(description)
            self.merchandise.setPrice(price)
            self.main_window.orderbox.append(self.merchandise)
        #    if self.notFromADialog:
                # Since the inventory won't disappear as a dialog, we need to 
                # remove the selected item from the list
         #       self.main_window.searchInventory.removeItem(self.merchandise.searchWindowIndex)
            self.EndModal(1)
            
        else:
            self.static3=wxStaticText(self, -1, "Fill in both fields!!!!",pos=wxPoint(15,170))
