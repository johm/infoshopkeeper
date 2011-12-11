from wxPython.wx import *
from infoshopkeeper_config import configuration
import string

class multiplePricesNotebook(wxNotebook):
    def __init__(self,**kwargs):
        wxNotebook.__init__(self,**kwargs)
        self.pages={}  #maps a name to a pricePage
#        EVT_NOTEBOOK_PAGE_CHANGED(self, self.GetId(), self.OnPageChanged) 


 #   def OnPageChanged(self, event): 
 #       event.Skip() 

    def hasPage(self,page_name=""):
        if page_name in self.pages.keys():
            return True
        else:
            return False

    def addPage(self,page_name="",proportion_of_master=1,master=False):
        if self.hasPage(page_name):
            raise RuntimeError, "you should check to see if the page already exists"
        else:
            the_page=wxTextCtrl(id=-1,name=page_name,parent=self,style=0,size=wxSize(200,35))
            self.pages[page_name]=the_page
            the_page.proportion_of_master=proportion_of_master
            the_page.master=master
            sizer=wxBoxSizer(wxHORIZONTAL)
            the_page.SetAutoLayout(1)
            the_page.SetSizer(sizer)
            #the_page.Fit()
            the_page.Layout()
            
            self.AddPage(the_page,page_name)
            if master:
                EVT_TEXT(self,the_page.GetId(),self.update_pages)

                
    def update_pages(self,event):
        print "HERE"
        master_page_name=[m for m in self.pages.keys() if self.pages[m].master][0]
        master_page=self.pages[master_page_name]
        new_master_price=float(string.replace(master_page.GetValue(),"$",""))
	cfg = configuration()
	for mp in cfg.get("multiple_prices"):
            if mp[0] != master_page_name:
                print mp[1]
                self.pages[mp[0]].SetValue("%s" % (mp[1]*new_master_price))
                
            
        

        
