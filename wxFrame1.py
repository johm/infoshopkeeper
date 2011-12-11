#Boa:Frame:wxFrame1

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

# Rough overview of the code structure:
#                                                   wxFrame1 
#                                        _________ /        \____________
#                                       /                                \
#                                      /                                  \
#                     Loads config to check the sizer list                 \
#                   (which is a list of preprogrammed panels        Loads some objects:-q
#                      designed for different actions)                                   |
#                      |                                                                 |
#                      |-> saved_sale can save and recall                                |
#                      |   saved sales                                                   |
#                      |-> sale is the current sale with some                            |
#                      |   buttons to pay cash, credit, etc.                             |
#                      |-> messager is a window to let message                           |
#                      |   to other volounteers                                          |
#                      |-> inventorysearch is a module to search
#                      |   books through the inventory
#                      |-> simple_items sell items that have a 
#                      |   constant price and are available at
#                      |   the ton, eg: coffee
#                      |-> complex_items sells objects that are
#                      |   counted and distinct, eg: t-shirts
#                      |-> misc_functions_menu and 
#                          misc_functions_notebook load the
#                          objects defined in misc_functions
#                                              \
#                                               `---> those objects refers
#                                              to the factories directory which 
#                                            contains class that most of the time
#                                         call popups defined in the popups directory
#                      
#


import string 
import types
from wxPython.wx import *
from wxPython.stc import *
from types import *

from infoshopkeeper_config import configuration
from displays.numericDisplay import numberbox
from displays.orderDisplay import orderbox

from components.item import item
from components.complex_item import complex_item
from components.item_merchandise import merchandise
from components.cashbox import cashbox
from components.memberslist import MembersList 
from components.inventory import inventory

from controls.NotesListBox import NotesListBox
from controls.simpleItemNotebook import simpleItemNotebook
from controls.complexItemNotebook import complexItemNotebook
from controls.miscFunctionNotebook import miscFunctionNotebook

from popups.searchinventorypanel import SearchInventoryPanel
from popups.cashdrawer import CashDrawerPopup
from popups.discount import DiscountPopup
from popups.cashpayment import CashPaymentPopup
from popups.checkout import CheckoutPopup
from popups.emprunt import CheckEmpruntPopup
from popups.checkin import CheckinPopup
from popups.receipt import ReceiptPopup

def create(parent):
    return wxFrame1(parent)



class wxFrame1(wxFrame):
    def _init_utils(self):
        # generated method, don't edit
        pass
    
    def _init_ctrls(self, prnt):
	self.cfg = configuration()
	title = self.cfg.get("title")
	wxFrame.__init__(self, id=-1, name='', parent=prnt,
			pos=wxPoint(35, 47), 
                        style=wxDEFAULT_FRAME_STYLE, title=title)
        self._init_utils()
        self.SetSizer(self.build_GUI()) 
        self.Fit()
        self.global_sizer.SetSizeHints(self)

    def __init__(self, parent):
	self.parent=parent
        self._init_ctrls(parent)
	self.orderboxes={
		"default":self.orderbox,
	}
        self.tab_list.Append("default","default")	
	
	self.current_orderbox_name="default"
        self.cashbox=cashbox()
        self.membersList=MembersList()
        self.inventory=inventory()
        self.Lower()
        win = CashDrawerPopup(self,self.cashbox)
        win.Fit()
        win.CenterOnScreen()
        
        #pos = self.ClientToScreen( (0,0) )
        #win.Position(pos, (100, 100))
        win.ShowModal()
        win.Destroy()
         


    def Generate_OnItem_Button(self,item_number):
        return lambda event : self.orderbox.append(item(item_number))

	
    def changeOrderBox(self,orderbox_name):
	self.order_list.Clear()
	self.orderbox=self.orderboxes[orderbox_name]
	self.orderbox.redisplay()
	self.current_orderbox_name=orderbox_name			
	
	self.tab_list.SetSelection(self.orderbox.list_position)	
	print "Setting selection to %s at %s " % (orderbox_name,self.orderbox.list_position)
	for k in self.orderboxes.keys():
		print "%s %s" %(k,self.orderboxes[k].list_position)

    def deleteOrderBox(self,orderbox_name):
	print "deleting orderbox %s" % orderbox_name
	removed=self.orderboxes[orderbox_name].list_position
	self.tab_list.Delete(self.orderboxes[orderbox_name].list_position)
	del self.orderboxes[orderbox_name]
	for obox_name in self.orderboxes.keys():
		obox=self.orderboxes[obox_name]
		if obox.list_position>removed:
			obox.list_position = obox.list_position - 1
	self.changeOrderBox("default")

#    def newOrderBox(self,orderbox_name):
#	self.orderboxes[orderbox_name]=orderbox(self.order_list,self)
#	self.orderbox=self.orderboxes[orderbox_name]	

    def saveOrderBox(self,orderbox_name):
	
	#if name was default
	if self.current_orderbox_name=="default":	
		self.orderboxes["default"]=orderbox(self.order_list,self,"default",0)
		# current orderbox gets a name
		self.orderboxes[orderbox_name]=self.orderbox	
		self.orderboxes[orderbox_name].list_position=self.tab_list.GetCount()

	else:
		self.orderboxes[orderbox_name]=orderbox(self.order_list,self,orderbox_name,self.tab_list.GetCount())	


	print "Saving tab %s with position %s" % (orderbox_name,self.orderboxes[orderbox_name].list_position);
	self.tab_list.Append(orderbox_name,orderbox_name)
	
	self.current_orderbox_name=orderbox_name	
	self.orderbox=self.orderboxes[orderbox_name]
        self.order_list.Clear()
        self.orderbox.redisplay()
	self.tab_list.SetSelection(self.orderbox.list_position)	


	print "SAVED %s at Position %s" %(orderbox_name,self.orderbox.list_position) 
	for k in self.orderboxes.keys():
		print "%s %s" %(k,self.orderboxes[k].list_position)
	

    


    def OnDiscountButton(self,event):
        win = DiscountPopup(self,5)
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
        


    def OnCredit_button(self, event):
        if self.orderbox.totaled == True:
            self.orderbox.finalize_items("credit")
            self.do_receiptPopup(event,"credit")
            self.display_field.SetValue("Order Paid: Credit")
        else:
            self.orderbox.displayFinalTotal()

    def OnCash_button(self, event):
        if self.orderbox.totaled == True:
            self.orderbox.finalize_items("cash")
            self.do_cashPaymentPopup(event,"cash")
            self.display_field.SetValue("Order Paid: Cash")
        else:
            self.orderbox.displayFinalTotal()

    def OnCheck_button(self, event):
        if self.orderbox.totaled == True:
            self.orderbox.finalize_items("check")
            self.do_receiptPopup(event,"check")
            self.display_field.SetValue("Order Paid: Check")
        else:
            self.orderbox.displayFinalTotal()

    def OnSaveOrder(self, event):
	if self.save_orderbox_name.GetValue()!="":
		self.saveOrderBox(self.save_orderbox_name.GetValue())
		self.save_orderbox_name.SetValue("")
	else:
		print "NO TAB NAME SPECIFIED"

    def do_receiptPopup(self,event,payment_info):
        win = ReceiptPopup(self,payment_info)

        # Show the popup right below or above the button
        # depending on available screen space...
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        #win.Position(pos, (0, sz.height))
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
        
    def do_cashPaymentPopup(self,event,payment_info):
        win = CashPaymentPopup(self,payment_info)

        # Show the popup right below or above the button
        # depending on available screen space...
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        #win.Position(pos, (0, sz.height))
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
        
    


    def OnTotal_buttonButton(self, event):
#        self.orderbox.addTax()
        self.orderbox.displayFinalTotal()
#        self.display_field.SetValue("Total: %.2f" % self.orderbox.getTotal())

    def OnSubTotal_buttonButton(self, event):
        self.display_field.SetValue("SubTotal: %.2f" % self.orderbox.getTotal())

    def OnRemove_buttonButton(self, event):
        self.orderbox.remove_selected()

    def OnVoid_button(self, event):
	print "voiding orderbox %s" % self.current_orderbox_name
	self.orderbox.void()
	if not(self.current_orderbox_name == "default"):
		self.deleteOrderBox(self.current_orderbox_name)        


    def OnCheckoutButton(self,event):
        
        if self.orderbox.isAllBorrowable() != True:
           dlg = wxMessageDialog(self, 'Mmmmm, some items might not be borrowed (maybe coffee ?)')
           dlg.ShowModal() 
        elif self.orderbox.isEmpty():
           dlg = wxMessageDialog(self, 'This system can\'t check out less than 1 items at a time')
           dlg.ShowModal() 
        else: 
            win = CheckoutPopup(self)
            btn = event.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            win.CenterOnScreen()
            win.ShowModal()
            win.Destroy()


    def OnCheckinButton(self,event):
        win = CheckEmpruntPopup(self)
        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()



    def OnOrderItemSelected(self,event):
        self.orderbox.select(event.GetSelection())

    def OnTabSelected(self,event):
	tab_number=event.GetSelection()
	print "Tab at position %s selected" % (tab_number) 
	self.changeOrderBox(self.tab_list.GetString(tab_number))
	print "Changing to tab " + self.tab_list.GetString(tab_number)
	
#	self.tab_list.Delete(tab_number)
    def sizer_add(self, sizer, args):
        if isinstance(args[0], StringTypes)!=true:
            item = args[0]
        elif args[0] == "saved_sale":
            item = self.make_saved_sale_sizer()
        elif args[0] == "sale":
            item = self.make_sale_sizer()
        elif args[0] == "inventory_search":
            item = self.make_inventory_search()
        elif args[0] == "simple_items_notebook":
            item = self.make_simple_items_notebook()
        elif args[0] == "complex_items_notebook":
            item= self.make_complex_items_notebook()
        elif args[0] == "misc_functions_menu":
            self.make_misc_functions_menu()
            self.SetMenuBar(self.misc_functions_menubar)
            return 
        elif args[0] == "misc_functions_notebook":
            item = self.make_misc_functions_notebook()
        elif args[0] == "messager":
            item = self.make_messager_sizer()
        else: 
            print "Invalid GUI items in configuration"
            return 
        if args[2]==1: 
            flags=wxGROW 
        else: 
            flags=0
        sizer.Add(item,
            flag= flags,
            proportion= args[1])

    def build_GUI(self):
        self.global_sizer= wxBoxSizer(wxHORIZONTAL)
        col_sizer = []
        orderboxAndSearchpanel = 0
        sizer_list = self.cfg.get("sizer_list")
	for x in range(len(sizer_list)):
            # This condition checks if the subarray is a subarray of box
            # definition or just a box definition
            if len(sizer_list[x])>3 and isinstance(sizer_list[x][0], StringTypes) != true:
                col_sizer.append(wxBoxSizer(wxVERTICAL))
                for y in range(len(sizer_list[x]) - 2):
                    # To put back the ordered items in the search box, we
                    # we need to know if we have both
                    if sizer_list[x][y][0] == "sale":
                        orderboxAndSearchpanel += 5
                    if sizer_list[x][y][0] == "inventory_search":
                        orderboxAndSearchpanel += 13
                    self.sizer_add(sizer=col_sizer[x], args=sizer_list[x][y])     
                self.sizer_add(sizer=self.global_sizer,
                            args=(col_sizer[x],
                            sizer_list[x][-2],
                            sizer_list[x][-1]))
            else:
                if sizer_list[x][0] == "sale":
                    orderboxAndSearchpanel += 5
                if sizer_list[x][0] == "inventory_search":
                    orderboxAndSearchpanel += 13
                self.sizer_add(sizer=self.global_sizer,
                    args=sizer_list[x])
                col_sizer.append(0)
        if orderboxAndSearchpanel == 18:
            self.orderbox.searchNotAsDialog = True
        return self.global_sizer

    def make_inventory_search(self):
        self.searchInventory = SearchInventoryPanel(parent=self)
        return self.searchInventory

    def make_saved_sale_sizer(self):
	# Make the box for the saved sales... 
        savedSaleSizer = wxStaticBoxSizer(wxStaticBox(parent=self, id=-1, label="Save sale"),
            wxHORIZONTAL)
        self.savedSaleAddSaleSizer = wxBoxSizer(wxVERTICAL) 
        self.save_order = wxButton(id=-1, label='run tab', name='save_order', parent=self, size=wxSize(110, 32), style=0)
        EVT_BUTTON(self.save_order, self.save_order.GetId(), self.OnSaveOrder)
        self.save_orderbox_name = wxTextCtrl(id=-1,name="save_orderboxname",parent=self,size=wxSize(110,32),style=wxTE_PROCESS_ENTER)
        EVT_TEXT_ENTER(self.save_orderbox_name, self.save_orderbox_name.GetId(),self.OnSaveOrder)
        self.savedSaleAddSaleSizer.Add(self.save_order);
        self.savedSaleAddSaleSizer.Add(self.save_orderbox_name);
        self.tab_list = wxListBox(choices=[], id=-1,
			name='tab_list', parent=self,
			size=wxSize(110, 65), style=wxLIST_FORMAT_RIGHT, validator=wxDefaultValidator)
        EVT_LISTBOX(self.tab_list, self.tab_list.GetId(), self.OnTabSelected)
        savedSaleSizer.Add(self.savedSaleAddSaleSizer)
        savedSaleSizer.Add(self.tab_list, flag=wxGROW, proportion=1) 
        return savedSaleSizer

    def make_sale_sizer(self):
        self.saleSizer = wxStaticBoxSizer(wxStaticBox(parent=self, id=-1, label="Current Sale"), wxVERTICAL)
        # this is for the upper buttons, stashed in saleUpperButtonSizer
        self.saleUpperButtonsSizer = wxFlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)
        self.checkout_button = wxButton(id=-1,
              label='check out', name='co_button', parent=self, 
              style=0)
        EVT_BUTTON(self.checkout_button, self.checkout_button.GetId(),
              self.OnCheckoutButton)

        self.checkin_button = wxButton(id=-1,
              label='check in', name='ci_button', parent=self, 
              style=0)
        EVT_BUTTON(self.checkin_button, self.checkin_button.GetId(),
              self.OnCheckinButton)

        self.remove_button = wxButton(id=-1,
              label='remove item', name='remove_button', parent=self, 
              style=0)
        EVT_BUTTON(self.remove_button, self.remove_button.GetId(),
              self.OnRemove_buttonButton)

        self.void_button = wxButton(id=-1,
              label='void entire\n sale', name='void_button', parent=self, 
              style=0)
        EVT_BUTTON(self.void_button, self.void_button.GetId(),
              self.OnVoid_button)
        self.saleUpperButtonsSizer.Add(self.checkout_button)
        self.saleUpperButtonsSizer.Add(self.checkin_button)
        self.saleUpperButtonsSizer.Add(self.remove_button)
        self.saleUpperButtonsSizer.Add(self.void_button)
         
	    # The order list and display list will be added as is in the
		# saleSizer, since they're alone on their lines...
        self.order_list = wxListBox(choices=[], id=-1,
              name='order_list', parent=self, 
              size=wxSize(200, 200), style=wxLIST_FORMAT_RIGHT, 
			  validator=wxDefaultValidator)
        EVT_LISTBOX(self.order_list, self.order_list.GetId(), self.OnOrderItemSelected)
		
        self.display_field = wxTextCtrl(id=-1,
              name='display_field', parent=self, 
              size=wxSize(200, 32), style=wxTE_PROCESS_ENTER, value='0')
        self.display_field.SetToolTipString('hi')
        self.display_field.SetInsertionPoint(0)
        self.display_field.Show(True)
        self.numberbox=numberbox(self.display_field) 
        self.orderbox=orderbox(self.order_list,self,"default",0)
 
        # The sale and discount buttons		
        self.saleLowerButtonsSizer = wxBoxSizer(wxHORIZONTAL) 
        self.total_button = wxButton(id=-1,
              label='subtotal', name='total_button', parent=self,
              size=wxSize(150, 32), style=0)
        EVT_BUTTON(self.total_button, self.total_button.GetId(),
              self.OnTotal_buttonButton)

        self.discount_button = wxButton(id=-1,
              label='discount', name='discount_button', parent=self,
              size=wxSize(55, 32), style=0)
        EVT_BUTTON(self.discount_button, self.discount_button.GetId(),
              self.OnDiscountButton)
        self.saleLowerButtonsSizer.Add(self.total_button)
        self.saleLowerButtonsSizer.Add(self.discount_button)

		# We make a grid for the payment mode, since there could be
		# more than 3 here
        self.salePaymentModeSizer = wxGridSizer(rows=1, cols=3, vgap=10, hgap=10)
        self.credit_button = wxButton(id=-1,
                                      label='credit', name='credit_button', parent=self, 
                                      size=wxSize(66, 32), style=0)
        EVT_BUTTON(self.credit_button, self.credit_button.GetId(),
                   self.OnCredit_button)

        self.cash_button = wxButton(id=-1,
                                      label='cash', name='cash_button', parent=self, 
                                      size=wxSize(66, 32), style=0)
        EVT_BUTTON(self.cash_button, self.cash_button.GetId(),
                   self.OnCash_button)

        self.check_button = wxButton(id=-1,
                                     label='check', name='check_button', parent=self,
                                     size=wxSize(66, 32), style=0)
        EVT_BUTTON(self.check_button, self.check_button.GetId(),
                   self.OnCheck_button)
        self.salePaymentModeSizer.Add(self.credit_button)
        self.salePaymentModeSizer.Add(self.cash_button)
        self.salePaymentModeSizer.Add(self.check_button)

        self.saleSizer.Add(self.saleUpperButtonsSizer)
        self.saleSizer.Add(self.order_list, proportion=1, flag=wxALIGN_CENTER|wxGROW)
        self.saleSizer.Add(self.display_field, flag=wxGROW)
        self.saleSizer.Add(self.saleLowerButtonsSizer)
        self.saleSizer.Add(self.salePaymentModeSizer, flag=wxGROW)
        return self.saleSizer

    def make_simple_items_notebook(self):
        simple_items = self.cfg.get("simple_items")
        self.simple_items_notebook=simpleItemNotebook(id=-1,name="si_notebook", parent=self)
        for x in range(len(simple_items)):	
            try:
                simple_items[x]
                page_name="stuff"

                try:
                    page_name=simple_items[x][3]["page"]                                
                except:
                    pass

                if (not(self.simple_items_notebook.hasPage(page_name))):
                    self.simple_items_notebook.addPage(page_name)
                    
                my_page=self.simple_items_notebook.pages[page_name]
                newButton = wxButton(id=-1,
                                 label=item(x).getLabel(),
                                 name='item_%i' % (x+1),
                                 parent=my_page,
                                 pos=wxPoint(100* (my_page.counter % 5), 32 * (my_page.counter / 5)),
				                 size=wxSize(100, 32), style=0)
                setattr(self,"item_%i" % (x+1), newButton)
                my_page.counter=my_page.counter+1
                EVT_BUTTON(getattr(self,"item_%i" % (x+1)),
                           getattr(getattr(self,"item_%i" % (x+1)),"GetId")(),
                           self.Generate_OnItem_Button(x))
                try:
                    getattr(self,"item_%i" % (x+1)).SetForegroundColour(simple_items[x][3]["color"])
                except:
                    a="no color"
            except:
                a="outofrange"
        return self.simple_items_notebook

    def make_complex_items_notebook(self):
        complex_items = self.cfg.get("complex_items")
        self.complex_items_notebook=complexItemNotebook(id=-1,name="co_notebook",parent=self)
        for x in range(len(complex_items)):	
            try:
                print complex_items[x]
                page_name="stuff"
		
                try:
                    page_name=complex_items[x][3]["page"]                                
                except:
                    pass

                if (not(self.complex_items_notebook.hasPage(page_name))):
                    self.complex_items_notebook.addPage(page_name)
                print "here"
                my_page=self.complex_items_notebook.pages[page_name]
                print "here2"
                setattr(self,"complexitem%i" % (x+1),
                        wxButton(id=-1,
                                 label=complex_item(x).getLabel(),
                                 name='complexitem%i' % (x+1),
                                 parent=my_page,
                                 pos=wxPoint(90* (my_page.counter % 3), 32 * (my_page.counter / 3)),
                                 size=wxSize(90, 32), style=0))
                my_page.counter=my_page.counter+1
                print "here3"
                print "factories." + complex_items[x][2]
                module4button=__import__("factories." + complex_items[x][2],globals(),[],[1])
                
		EVT_BUTTON(getattr(self,"complexitem%i" % (x+1)),
                           getattr(getattr(self,"complexitem%i" % (x+1)),"GetId")(),
                           module4button.GenerateOnPress(self,complex_item(x).getLabel()))
            
                try:
                    getattr(self,"complexitem%i" % (x+1)).SetForegroundColour(complex_items[x][3]["color"])
                except:
                    a="no color"
            except:
                a="outofrange"
                print a
        return self.complex_items_notebook
    
    def make_misc_functions_notebook(self):
        return self.make_misc_functions("notebook")
    def make_misc_functions_menu(self):
        return self.make_misc_functions("menu")

    def make_misc_functions(self, type):
        self.modulefunc = {}
	module4button = {}
        misc_functions = self.cfg.get("misc_functions")
	if type == "notebook":
            self.misc_functions_notebook=miscFunctionNotebook(id=-1,name="misc_notebook",parent=self)
	if type == "menu":
	    self.misc_functions_menubar=wxMenuBar()
	    self.menu = {}
        for x in range(len(misc_functions)):	
	    # page name here refer either to the name of the default menu
	    # or the default page
            page_name="tasks"
            try:
                page_name=misc_functions[x][3]["page"]
            except:
                pass
            print "adding "+misc_functions[x][0]+" on "+page_name
            # Create the object that will be clicked on
	    if type == "notebook": 
		if not(self.misc_functions_notebook.hasPage(page_name)):
                    self.misc_functions_notebook.addPage(page_name)
                my_page=self.misc_functions_notebook.pages[page_name]
                # John, shall we use an array here instead of setattr ?
	        setattr(self,"miscfunc%i" % (x+1),
                        wxButton(id=-1,
                        label=misc_functions[x][0],
                        name='miscfunc%i' % (x+1),
                        parent=my_page,
                        pos=wxPoint(0, 32 * (my_page.counter)),
                        size=wxSize(180, 32), style=0))
                my_page.counter=my_page.counter+1
            if type == "menu": 
	        if not self.menu.has_key(page_name):
                    self.menu[page_name] = wxMenu()
                the_menu = self.menu[page_name].Append(x+99, misc_functions[x][0], misc_functions[x][2])
            # Load the function from the factory it comes
            try:
	        modul = __import__('factories.'+misc_functions[x][1], globals(),[],[1])
	    except:    
                print "Factory %s crashed when opening it... " % misc_functions[x][1]
	        import sys
		print sys.exc_info()[0]
	        raise

            try:
	        clas = getattr(modul, misc_functions[x][2])
	    except:    
	 	print "Class " + misc_functions[x][2] + "isn't defined in the factory " + misc_functions[x][1]
            try:
	        module4button[x] = clas()
	    except:
                print "Class %s have crashed when initialized. It was loaded from %s." % (misc_functions[x][2], misc_functions[x][1])
	        import sys
		print sys.exc_info()[0]
	        raise
            try:
                self.modulefunc[x] = module4button[x].GenerateOnPress(self, misc_functions[x][0])
	    except:  
                print "Factory %s GenerateOnPress function doesn't work " % misc_functions[x][2]
	        import sys
		print sys.exc_info()[0]
	        raise
            if type == "notebook":
   	        EVT_BUTTON(getattr(self,"miscfunc%i" % (x+1)),
                       getattr(getattr(self,"miscfunc%i" % (x+1)),"GetId")(),
                       self.modulefunc[x])
            if type == "menu":
		self.Bind(wx.EVT_MENU,  self.modulefunc[x], id=x+99)
            try:
                getattr(self,"miscfunc%i" % (x+1)).SetForegroundColour(misc_functions[x][3]["color"])
            except:
                a="no color"
	if type == "menu":
            for key, val in self.menu.iteritems():
	        self.misc_functions_menubar.Append(self.menu[key], key)
            return_value = self.misc_functions_menubar
	if type == "notebook":
	    return_value = self.misc_functions_notebook
	return return_value

 
    def make_messager_sizer(self):        
        # The code for the messager system...
        messagerSizer = wxBoxSizer(wxVERTICAL)
        self.note_list = NotesListBox(choices=[], id=-1,
              name='note_list', parent=self,
              size=wxSize(180, 200), style=wxLIST_FORMAT_RIGHT, validator=wxDefaultValidator)
        self.note_list.initialize(self)

        self.messageTextCtrl = wxTextCtrl(self, -1, "",size=(180, 50),
						style=wxTE_MULTILINE)
        self.messageAuthorLabel = wxStaticText(self,-1,"your name:")
        self.messageAuthorTextCtrl = wxTextCtrl(self, -1,
                        "",size=(92, -1))

        self.leaveMessage = wxButton(self,-1,"leave a message",size=(180,-1))
        EVT_BUTTON(self.leaveMessage,self.leaveMessage.GetId(),self.note_list.addmessage)
        messagerSizer.Add(self.note_list, proportion=1, flag=wxGROW)
        messagerSizer.Add(self.messageAuthorLabel)
        messagerSizer.Add(self.messageAuthorTextCtrl)
        messagerSizer.Add(self.messageTextCtrl)
        messagerSizer.Add(self.leaveMessage)
        return messagerSizer

