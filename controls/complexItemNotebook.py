from wxPython.wx import *

class complexItemNotebook(wxNotebook):
    def __init__(self,**kwargs):
        wxNotebook.__init__(self,**kwargs)
        self.pages={}  #maps a name to a complexItemNotebookPage


    def hasPage(self,page_name=""):
        if page_name in self.pages.keys():
            return True
        else:
            return False

    def addPage(self,page_name=""):
        if self.hasPage(page_name):
            raise RuntimeError, "you should check to see if the page already exists"
        else:
            the_page=complexItemNotebookPage(id=-1,name=page_name,parent=self,pos=wxPoint(300, 464),size=wxSize(275, 128),style=wxCLIP_CHILDREN | wxSW_3D)
            self.pages[page_name]=the_page
            self.AddPage(the_page,page_name)


class complexItemNotebookPage(wxSashWindow):
    def __init__(self,**kwargs):
        wxSashWindow.__init__(self,**kwargs)
        self.counter=0 #where we are in buttons

