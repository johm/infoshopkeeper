from wxPython.wx import *
from wxPython.wizard import *
from objects.title import Title
from objects.kind import Kind
from components.inventory import inventory
from components.item_inventoried_merchandise import inventoried_merchandise
from popups.inventoriedmerchandise import InventoriedMerchandisePopup


def GenerateOnPress(frame_object,label):
    return lambda event : do_easyselect_wizard(frame_object,event,label)

def do_easyselect_wizard(frame_object,event,label):
    wizard = EasySelectWizard (None, -1, label)
    wizard.label=label
    wizard.parent=frame_object
    if Kind.select(Kind.q.kindName==label).count()<1:
        print 'you probably need to add a kind to correspond to the label %s' % label

    title_list=Title.select("""
    title.kind_id= kind.id AND
    kind.kind_name='%s'
    """ % (label),orderBy=Title.q.booktitle,clauseTables=['kind'],distinct=True)
    
    #wizard.title_list=[t for t in title_list if len([b for b in t.books if b.status=="STOCK"])>0] 
    wizard.title_list=title_list 

    wizard.title_page = ChooseItemPage ( wizard )
    wizard.GetPageAreaSizer().Add(wizard.title_page)
    wizard.action_page=ChooseActionPage(wizard)
    EVT_WIZARD_FINISHED(wizard,wizard.GetId(), wizard.finish)
    wizard.RunWizard ( wizard.title_page )
    wizard.Destroy()


class EasySelectWizard(wxWizard):
    
    def finish(self,event):
        title=None
        copy=None

        if self.action_page.return_copies.GetValue()==True:
            return_to=self.action_page.return_to.GetStringSelection()
            return_x=int(self.action_page.return_x.GetValue())
            return_these_books=[b for b in self.which_title.books if b.status=="STOCK" and b.distributor==return_to][0:return_x]
            for b in return_these_books:
                b.change_status("RETURN")
            

        if self.action_page.inventory_copies.GetValue()==True:
            known_title=False
            new_title_name=""
            if self.title_page.new_title.GetValue()==True:
                new_title_name=self.title_page.enter_new_title.GetValue()
            else:
                known_title=self.which_title


            inventory().addToInventory(title=new_title_name,price=float(self.action_page.inventory_price.GetValue()),distributor=self.action_page.inventory_from.GetValue(),quantity=self.action_page.inventory_x.GetValue(),known_title=known_title,kind_name=self.label)


        if self.action_page.sell_a_copy.GetValue()==True:
            m_item=inventoried_merchandise(self.label)
            m_item.set_title_and_copy(self.which_copy)
        
            win = InventoriedMerchandisePopup(self.parent,m_item,self.parent)

            win.CenterOnScreen()
            win.ShowModal()
            win.Destroy()


            



class ChooseItemPage ( wxPyWizardPage ):

   def __init__ ( self, parent ):

      # Call __init__

      wxPyWizardPage.__init__ ( self, parent )

      self.parent=parent
            
      # Specify None for the next and previous pages

      self.next = None

      self.previous = None

      self.sizer = wxGridBagSizer ( 2, 10 )

      # Create one group of buttons ( plus a label ) and add them

      # We mark the beginning of the group with wxRB_GROUP

      self.existing_title = wxRadioButton ( self, -1, 'Select an existing title', style = wxRB_GROUP )


      
      titles=[t.booktitle for t in parent.title_list]
      
      self.select_existing_title=wxListBox(self,-1,choices=titles,size=wxSize(180,200))

      self.new_title = wxRadioButton ( self, -1, 'Add a new title' )
      EVT_RADIOBUTTON ( self, self.new_title.GetId(), self.selected_new_title)
      EVT_RADIOBUTTON ( self, self.existing_title.GetId(), self.selected_existing_title)
      EVT_LISTBOX(self,self.select_existing_title.GetId(),self.existing_title_picked)
            
      self.enter_new_title=wxTextCtrl(self,-1,size=wxSize(180,32))

      self.sizer.Add(self.existing_title,(0,0))
      self.sizer.Add(self.select_existing_title,(1,0))


      self.sizer.Add(self.new_title,(3,0))
      self.sizer.Add(wxStaticText(self,-1,'New title name:'),(4,0))
      self.sizer.Add(self.enter_new_title,(5,0))
      self.enter_new_title.Disable()

      self.SetSizerAndFit ( self.sizer )

      # Resize the window

      self.sizer.Fit ( self )


   def existing_title_picked(self,event):
       title_index=self.select_existing_title.GetSelections()[0]
       self.parent.which_title=self.parent.title_list[title_index]
       self.parent.action_page.sell_a_copy.Enable()
       self.parent.action_page.return_copies.Enable()
       self.parent.which_copy=[b for b in self.parent.which_title.books if b.status=="STOCK"][0]
       

   def selected_new_title(self,event):
       self.select_existing_title.Disable()
       self.enter_new_title.Enable()       
       self.parent.action_page.sell_a_copy.Disable()
       self.parent.action_page.return_copies.Disable()

       
       
   def selected_existing_title(self,event):
       self.enter_new_title.Disable()
       self.select_existing_title.Enable()

   def GetNext ( self ):
       return self.parent.action_page


   def GetPrev ( self ):

      return self.previous




class ChooseActionPage ( wxPyWizardPage ):

   def __init__ ( self, parent ):

      # Call __init__

      wxPyWizardPage.__init__ ( self, parent )

      self.parent=parent

      # Specify None for the next and previous pages

      self.next = None

      self.previous = None

      self.sizer = wxGridBagSizer ( 6, 10 )



      # We mark the beginning of the group with wxRB_GROUP

      self.sell_a_copy = wxRadioButton ( self, -1, 'Sell a copy', style = wxRB_GROUP )

      self.inventory_copies = wxRadioButton ( self, -1, 'Inventory' )
      self.inventory_x = wxTextCtrl(self,-1,value='1')
      self.inventory_from = wxTextCtrl(self,-1)
      self.inventory_price = wxTextCtrl(self,-1)
      
      

      self.return_copies = wxRadioButton ( self, -1, 'Return' )
      self.return_x = wxTextCtrl(self,-1,value='1')
      self.return_to = wxChoice(self,-1)
      


      EVT_RADIOBUTTON ( self, self.sell_a_copy.GetId(), self.selected_sell_a_copy)
      EVT_RADIOBUTTON ( self, self.inventory_copies.GetId(), self.selected_inventory_copies)
      EVT_RADIOBUTTON ( self, self.return_copies.GetId(), self.selected_return_copies)


            

      self.sizer.Add(self.sell_a_copy,(0,0))

      self.sizer.Add(self.inventory_copies,(1,0))

      self.sizer.Add(self.inventory_x,(2,0))
      self.sizer.Add(wxStaticText(self,-1,'copies from'),(2,1))
      self.sizer.Add(self.inventory_from,(2,2))
      self.sizer.Add(wxStaticText(self,-1,'@ $'),(2,3))
      self.sizer.Add(self.inventory_price,(2,4))

      

      self.sizer.Add(self.return_copies,(3,0))

      self.sizer.Add(self.return_x,(4,0))
      self.sizer.Add(wxStaticText(self,-1,'copies to'),(4,1))
      self.sizer.Add(self.return_to,(4,2))
      
      self.inventory_x.Disable()
      self.inventory_from.Disable()
      self.return_x.Disable()
      self.return_to.Disable()
      
      self.SetSizerAndFit ( self.sizer )

      # Resize the window

      self.sizer.Fit ( self )



   def selected_sell_a_copy(self,event):
       self.inventory_x.Disable()
       self.inventory_from.Disable()
       self.return_x.Disable()
       self.return_to.Disable()

   def selected_inventory_copies(self,event):
       self.inventory_x.Enable()
       self.inventory_from.Enable()
       self.return_x.Disable()
       self.return_to.Disable()
       

   def selected_return_copies(self,event):
       self.inventory_x.Disable()
       self.inventory_from.Disable()
       self.return_x.Enable()
       self.return_to.Enable()
       
   


   def GetNext ( self ):
       return None


   def GetPrev ( self ):

      return self.parent.title_page





