from wxPython.wx import *
from infoshopkeeper_config import configuration
import string
cfg = configuration()

class aPrice(wxPanel):
    def __init__(self,**kwargs):
        wxPanel.__init__(self,**kwargs)
        self.price_ctrl=wxTextCtrl(id=-1,parent=self,style=0,size=wxSize(200,35),pos=(0,40))
        self.proportion_ctrl=wxTextCtrl(id=-1,parent=self,style=0,size=wxSize(200,35))
        
    def __cmp__(self,other):
        if self.master:
            return -1
        if other.master:
            return 1
        return cmp(self.page_name,other.page_name)
        
class multiplePrices:
    def __init__(self,parent):
        self.mp_sizer=wxGridSizer(2,2,2,2)
        self.parent=parent
        self.pages={}  #maps a name to a pricePage
        
    def hasPage(self,page_name=""):
        if page_name in self.pages.keys():
            return True
        else:
            return False

    def addPage(self,page_name="",proportion_of_master=1,master=False):
        if self.hasPage(page_name):
            raise RuntimeError, "you should check to see if the page already exists"
        else:
            the_page=aPrice(id=-1,name=page_name,parent=self.parent,style=0)
            self.pages[page_name]=the_page
            the_page.page_name=page_name
            the_page.proportion_ctrl.SetValue("%s" % (proportion_of_master))
            the_page.master=master
#            sizer=wxBoxSizer(wxHORIZONTAL)
#            the_page.SetAutoLayout(1)
#            the_page.SetSizer(sizer)
#            the_page.Fit()
#            the_page.Layout()

#            self.AddPage(the_page,page_name)
            if master:
                the_page.proportion_ctrl.Disable()
                EVT_TEXT(the_page.price_ctrl,the_page.price_ctrl.GetId(),self.update_pages)
            else:
                EVT_TEXT(the_page.proportion_ctrl,the_page.proportion_ctrl.GetId(),self.update_pages)

    def render(self):
        pages=self.pages.values()
        pages.sort()
        page_names=[p.page_name for p in pages]
        for page_name in page_names:
            self.mp_sizer.Add(wxStaticText(self.parent,-1,page_name))
        for page_name in page_names:
            self.mp_sizer.Add(self.pages[page_name])
    
    def update_pages(self,event):
        master_page_name=[m for m in self.pages.keys() if self.pages[m].master][0]
        master_page=self.pages[master_page_name]
        try:
	    new_master_price=float(string.replace(master_page.price_ctrl.GetValue(),"$",""))
	except ValueError: 
	    # The user has written non integer in the price value
            new_master_price = 0
	for mp in cfg.get("multiple_prices"):
            if mp[0] != master_page_name:
                self.pages[mp[0]].price_ctrl.SetValue("%s" % (float(self.pages[mp[0]].proportion_ctrl.GetValue())*new_master_price))
	    
        
