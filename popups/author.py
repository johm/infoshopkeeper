# Copyright 2006 Guillaume Beaulieu
# but almost everything is cut and pasted from code by john

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

# I've crammed here the code for searchmemberpopup, addmemberpopup,
# addmemberpanel and browsememberpanel. Those panel are distinct since
# they are used in the checkout popup. Panel are at the end, since 
# they have ugly code...

# Members will be used checking out books only to members of a
# library

from wxPython.lib.mixins.listctrl import wxColumnSorterMixin


from objects.title import Title
from objects.author import Author

from wxPython.wx import *
import etc
import string

import os

# Da plan:
#
#                          BOOKANDAUTHORJOINA
#  ______________________________/\________________________________
# /                                                                \
#  
# ALLAUTHORLIST            MOVINGDEVICE             CURRENTAUTHORLIST
#
# AUTHOR LIST      |     THROW SELECTED AUTHOR     | BOOK NAME 
# AUTHOR NAME 1    | THAT WAY------------------->  | CURRENT AUTHOR 1
# AUTHOR NAME 2    | <---------------- OR THAT WAY | CURRENT AUTHOR 2
# AUTHOR NAME 3    |                               | CURRENT AUTHOR 3   
# AUTHOR NAME 4    |  ADD AUTHOR [_________]       | 
# AUTHOR NAME 5    |  <--------- THERE             |
# AUTHOR NAME 6    |                               | 
# AUTHOR NAME 7    | <- BAN THIS AUTHOR FOREVER    | 
# AUTHOR NAME 8    |                               |
#
#
#
# The plan is to return a list of authorID wich will be added to the 
# book when the save button's will be clicked. The currently selected 
# author isn't saved anywhere else than in the current author list
# listCtrl
#
# There should be at some point complexification required for the 
# authors. For example, we should separate the first_name from
# the last name, and the middle initials and stuff. We should also
# have the year of birth and the year of death in the case of authors
# having the same names

class AuthorListCtrl(wxListCtrl):
    def __init__(self, parent, ID, pos=wxDefaultPosition, size=wxSize(),
                  style=0):
        wxListCtrl.__init__(self, parent, ID, pos, size=size,style=style)


class ChooseAuthorsPopup(wxDialog):
    def __init__(self,parent, func):
        self.parent = parent 
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Author list selection")
        self.sizer = wxBoxSizer(wxHORIZONTAL)
	self.panel = bookAndAuthorJoina(parent=self, main_window=self, execWhenSelected=func)
	self.sizer.Add(self.panel, flag=wxGROW)
	self.SetSizer(self.sizer)
	self.Fit()

    def OnCancel(self,event):
        self.EndModal(1)

class bookAndAuthorJoina(wxPanel):
    def __init__(self,parent, main_window, on_successful_add=false, execWhenSelected=None):
	self.parent = parent
	wxPanel.__init__(self, parent )
        self.on_successful_add=on_successful_add
        self.main_window = main_window
	self.execWhenSelected = execWhenSelected
        # ALL AUTHOR LISTS
        self.master_sizer=wxBoxSizer(wxHORIZONTAL)
        self.allAuthorList = AuthorListCtrl(self, wxNewId(),
                                 style=wxLC_REPORT | wxSUNKEN_BORDER
                                 | wxLC_EDIT_LABELS
                                 )
        self.allAuthorList.InsertColumn(0, "Author")
        self.allAuthorList.SetColumnWidth(0, wxLIST_AUTOSIZE_USEHEADER)
        self.master_sizer.Add(self.allAuthorList, flag=wxGROW, proportion=1)
	# Adding each authors 1 by 1 to the all author list
	self.loadAllAuthors()
	
	# MOVING DEVICE
	self.movingDevice = wxBoxSizer(wxVERTICAL)
        self.buttonFromAllToCurrent = wxButton(self, -1, "--Add author to current book author-->")
        EVT_BUTTON(self, self.buttonFromAllToCurrent.GetId(), self.OnAddToCurrent)
        self.buttonRemoveFromCurrent = wxButton(self, -1, "<--Remove author from current book--")
        EVT_BUTTON(self, self.buttonRemoveFromCurrent.GetId(), self.OnRemoveFromCurrent)
  	self.movingDevice.Add(self.buttonFromAllToCurrent,1,flag=wxGROW)
  	self.movingDevice.Add(self.buttonRemoveFromCurrent,1,flag=wxGROW)
	# ADDING AUTHOR DEVICE
        self.authorAddSizer = wxBoxSizer(wxHORIZONTAL)
        self.static1=wxStaticText(self, -1, "Author name")
	self.author_name=wxTextCtrl(id=-1,name="author_name", parent=self, style=wxTE_PROCESS_ENTER)
#        EVT_TEXT(self, self.author_name.GetId(), self.OnWrite) 
        self.authorAddSizer.Add(self.static1,0,wxEXPAND|wxALL,5)
        self.authorAddSizer.Add(self.author_name,1,wxEXPAND,5)
        self.movingDevice.Add(self.authorAddSizer, 1, flag=wxGROW)
        self.row3 = wxBoxSizer(wxHORIZONTAL)
	self.add_author = wxButton(self, -1, "Add Author")
	EVT_BUTTON(self, self.add_author.GetId(), self.OnAdd)
        self.cancel = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, self.cancel.GetId(), self.OnCancel)
        self.save = wxButton(self, -1, "Save")
        EVT_BUTTON(self, self.save.GetId(), self.OnSave)
        self.row3.Add(self.add_author, 2, wxGROW)
        self.row3.Add(self.save, 1, wxGROW)
        self.row3.Add(self.cancel, 1, wxGROW)
        self.movingDevice.Add(self.row3,1,wxEXPAND|wxALL,5)
	self.master_sizer.Add(self.movingDevice,1,wxEXPAND|wxALL,5)
        # CURRENT AUTHOR LIST
	self.currentAuthorList = AuthorListCtrl(self, wxNewId(),
                                 style=wxLC_REPORT | wxSUNKEN_BORDER
                                 | wxLC_EDIT_LABELS
                                 )
        self.currentAuthorList.InsertColumn(0, "Author")
        self.currentAuthorList.SetColumnWidth(0, wxLIST_AUTOSIZE)
        self.master_sizer.Add(self.currentAuthorList, flag=wxGROW, proportion=1)
       	self.SetSizer(self.master_sizer) 
	return None
    
    def loadAllAuthors(self):
	self.allAuthorList.DeleteAllItems()
	theAuthors = list(Author.select())
	i = 0
	for author in theAuthors:
	    print author
            self.allAuthorList.InsertStringItem(i,author.author_name.decode("string_escape"))
	    i = i + 1
	self.allAuthorList.SetColumnWidth(0, wxLIST_AUTOSIZE)
    
    def OnAddToCurrent(self,event):
        item = -1
	for i in range(0,self.allAuthorList.GetSelectedItemCount()):
	    item = self.allAuthorList.GetNextItem(item, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED);
	    self.currentAuthorList.InsertStringItem(0, self.allAuthorList.GetItemText(item))
        self.currentAuthorList.SetColumnWidth(0, wxLIST_AUTOSIZE)
    
    def OnRemoveFromCurrent(self,event):
        item = -1
	for i in range(0,self.currentAuthorList.GetSelectedItemCount()):
	    item = self.currentAuthorList.GetNextItem(item, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED);
	    self.currentAuthorList.DeleteItem(item)
    
    
    def OnSave(self,event):
    	# Here we need to translate the list of author that are
	# currently selected to a list of author_id
	if self.currentAuthorList.GetItemCount() == 0:
	    a = wxMessageDialog(self, "Can't save an empty author list, create an anonymous author and set him at least as the author", "Error", wxOK + wxICON_ERROR)
	    a.ShowModal()
	else:
	    list_of_author = []
            item = -1
	    # For all the authors in the list of authors
	    for i in range(0,self.allAuthorList.GetSelectedItemCount()):
	        item = self.allAuthorList.GetNextItem(item, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED);
	        # Get the name of the author
		his_name = self.allAuthorList.GetItemText(item).encode("ascii", "backslashreplace")
		# and try to find the name in the database. if there is
		# multiple, we just don't care
		#try: 
	        a = Author.selectBy(author_name = his_name)
		b = list(a)
		print b
		print b[0]
		list_of_author.append(b[0].id)
	        #except:
	        #    print his_name
	        #    print "Something real weird happened"
	    print list_of_author 
            self.parent.list_of_author = list_of_author
	    self.execWhenSelected(list_of_author)
	    self.parent.OnCancel(event)

    def OnCancel(self,event):
        self.parent.OnCancel(event)
 
    def OnWrite(self, event):
# This is postponed for next year...
#        in_list = self.allAuthorList.FindItem(-1, self.author_name.GetValue(), True)
	print in_list
#	if in_list != -1:
#	    self.allAuthorList.SetItemState(in_list, wxLIST_STATE_SELECTED, wxLIST_MASK_STATE)

    def OnAdd(self,event):
   	a = Author.selectBy(author_name = self.author_name.GetValue().encode("ascii", "backslashreplace"))
	if len(list(a)) != 0:
	    a = wxMessageDialog(self, "This author is already in the list", "Error", wxOK + wxICON_ERROR)
	    a.ShowModal()
	else:
	    a = Author(author_name = self.author_name.GetValue().encode("ascii", "backslashreplace"))
	    # This call deleteallitems on the author list. This is bad if there is a large amount of
	    # authors, we should simply add the new one.
	    self.loadAllAuthors() 

