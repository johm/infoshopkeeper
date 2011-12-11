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
from wxPython.lib.mixins.listctrl import wxColumnSorterMixin, wxListCtrlAutoWidthMixin
from popups.searchinventorypanel import SearchInventoryPanel, InventoryListCtrl


class SearchInventoryPopup(wxDialog,wxColumnSorterMixin):
    def GetListCtrl(self):
        return self.stuff.list
    
    def __init__(self,parent):
        self.parent=parent
        wxDialog.__init__(self, parent, -1, "Search inventory")
        self.SetSize(wxSize(800,600))
        self.browser = 0
        self.stuff = SearchInventoryPanel(parent=self,
                                is_dialog=1)
        
    def close_the_window(self):
        self.EndModal(1)

