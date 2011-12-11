from wxPython.wx import *

import textwrap

class wrappingListBox(wxListBox):
    def Append(self,str):
        newstr=textwrap.fill(str,30)
        lines=newstr.splitlines()
        for l in lines:
            wxListBox.Append(self,l)
