# Copyright 2008 John Duda 

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



import os
import string 
import types
from wxPython.wx import *
from wxPython.stc import *
from types import *
from upc import upc2isbn
econoscan=True

from infoshopkeeper_config import configuration


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
        
        self.Fit()


    def __init__(self, parent):
	self.parent=parent
        self._init_ctrls(parent)
        self.keybuffer=""
        self.static0=wxStaticText(self, -1, "Item ID (UPC or ISBN):")

        self.number=wxTextCtrl(id=-1,name="merchandise_id", parent=self, style=wxTE_PROCESS_ENTER)
        EVT_TEXT(self,self.number.GetId(), self.OnText)
        EVT_TEXT_ENTER(self,self.number.GetId(), self.OnTextEnter)
        EVT_CHAR(self.number, self.OnKeyDown)

        self.master_sizer=wxBoxSizer(wxVERTICAL)
        self.master_sizer.Add(self.static0,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.number,0,wxEXPAND|wxALL,5)
	self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)



    def OnKeyDown(self,event):
        keycode = event.GetKeyCode()
        if event.AltDown() == 1:
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


    def OnText(self,event):
        id=self.number.GetValue()
        if len(id) == 13:
		id=upc2isbn(id)			
		self.OnTextEnter(event)

    def OnTextEnter(self,event):
        id=self.number.GetValue()
        if len(id)==13 or len(id)==18:
	   	id=upc2isbn(id)				
        #here you want to set browser.link.open_external=0 in about:config in firefox
        cmd="http://localhost:8081/private/reinventory?isbn=%s" % (id)
	os.spawnlp(os.P_NOWAIT, "/usr/bin/firefox","/usr/bin/firefox",cmd )
        status = os.system(cmd)
        self.number.SetValue("")
        
