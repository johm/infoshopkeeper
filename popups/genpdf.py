# Copyright 2006 Guillaume Beaulieu 

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

import types
from infoshopkeeper_config import configuration
from wxPython.wx import *
from reports.PdfReport import PdfReport
cfg = configuration()

class GenPdfPopup(wxDialog):
    def GetListCtrl(self):
        return self.stuff.list
    
    def __init__(self,parent):
        self.parent=parent
        wxDialog.__init__(self, parent, -1, "Generate pdf reports")
        self.browser = 0
        self.stuff = GenPdfPanel(parent=self,
                                is_dialog=1)
        
    def close_the_window(self):
        self.EndModal(1)

class GenPdfPanel(wxPanel):
    
    def GetListCtrl(self):
        return self.list
    
    def __init__(self,parent, is_dialog=0):
        self.parent=parent
	self.maker = PdfReport()
        self.is_dialog = is_dialog
        if is_dialog:
            self.main_window = parent.parent
        else:
            self.main_window = parent
        self.browser = 0
        wxPanel.__init__(self, parent)
        tID = wxNewId()

        self.master_sizer=wxBoxSizer(wxVERTICAL)
        self.row_1=wxBoxSizer(wxHORIZONTAL)
        self.row_2=wxBoxSizer(wxHORIZONTAL)
        self.row_3=wxBoxSizer(wxHORIZONTAL)
        self.row_4=wxBoxSizer(wxHORIZONTAL)
        self.row_4etdemi=wxBoxSizer(wxHORIZONTAL) # et demi means and a half
        self.row_5=wxBoxSizer(wxHORIZONTAL)

	self.static3=wxStaticText(self, -1, "Period:")
        self.static4=wxStaticText(self, -1, "Report type")
        self.row_1.Add(self.static3,1,wxEXPAND,2)
        self.row_1.Add(self.static4,1,wxEXPAND,2)
        
        self.period=wxChoice(id=-1,name="period", parent=self,  style=0)
	self.period.Insert("Last Day", 0)
	self.period.Insert("Last Week", 0)
	self.period.Insert("Last Month", 0)
	self.period.Insert("Last Year", 0)
	self.period.Insert("Other", 0)
	
	EVT_CHOICE(self, self.period.GetId(), self.OnChoosePeriod)
       	self.period.SetSelection(0) # Set selection to Specify

	self.script=wxChoice(id=-1,name="script", parent=self, style=0, choices =  cfg.get("reports"))
	self.script.SetSelection(0)
	EVT_CHOICE(self, self.script.GetId(), self.OnChooseScript)
        
	self.row_2.Add(self.period,1,wxEXPAND|wxALL,5)
        self.row_2.Add(self.script,1,wxEXPAND|wxALL,5)
 
        self.static1=wxStaticText(self, -1, "Begin Date")
        self.static2=wxStaticText(self, -1, "End Date")
        self.row_3.Add(self.static1,1,wxEXPAND,2)
        self.row_3.Add(self.static2,1,wxEXPAND,2)
        
        self.begin_date=wxDatePickerCtrl(id=-1,name="begin_date", parent=self,  style=0)
	self.begin_date.SetValue(wxDateTime.Now())
	EVT_DATE_CHANGED(self, self.begin_date.GetId(), self.OnDateChange)
        self.end_date=wxDatePickerCtrl(id=-1,name="end_date", parent=self, style=0)
	self.end_date.SetValue(wxDateTime.Now())
	EVT_DATE_CHANGED(self, self.end_date.GetId(), self.OnDateChange)

        self.row_4.Add(self.begin_date,1,wxEXPAND,2)
        self.row_4.Add(self.end_date,1,wxEXPAND,2)
	
	self.row_4etdemi=wxBoxSizer(wxHORIZONTAL)
       	self.fichierSel = wxButton(self, -1, "Select File")
        EVT_BUTTON(self, self.fichierSel.GetId(), self.OnSelectFile)
        self.fichierText = wxTextCtrl(self, -1, name="nom_fichier", style=0)
        self.row_4etdemi.Add(self.fichierSel,1,wxEXPAND,2)
        self.row_4etdemi.Add(self.fichierText,1,wxEXPAND,2)
	
	self.fichierText.SetValue(self.maker.fileManager.getFileName(self.script.GetStringSelection(), self.period.GetStringSelection(), [self.begin_date.GetValue().FormatISODate(), self.end_date.GetValue().FormatISODate()]))
       
        self.b = wxButton(self, -1, "Cancel")
        EVT_BUTTON(self, self.b.GetId(), self.OnCancel)
        self.b2 = wxButton(self, -1, "Generate and open")
        EVT_BUTTON(self, self.b2.GetId(), self.OnGenerateAndShow)
        self.b3 = wxButton(self, -1, "Generate")
        EVT_BUTTON(self, self.b3.GetId(), self.OnGenerate)
        self.b2.SetDefault()
        self.row_5.Add(self.b3,0,wxEXPAND|wxALL,5)
        self.row_5.Add(self.b2,0,wxEXPAND|wxALL,5)
        self.row_5.Add(self.b,0,wxEXPAND|wxALL,5)
       
        self.master_sizer.Add(self.row_1,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_2,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_3,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_4,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_4etdemi,0,wxEXPAND|wxALL,5)
        self.master_sizer.Add(self.row_5,0,wxEXPAND|wxALL,5)
        self.statusBar = wxStatusBar(self, -1, name="statusBar")
        self.master_sizer.Add(self.statusBar,0,wxEXPAND|wxALL)

        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)
    
    def OnDateChange(self, event):
    	a = self.period.GetStringSelection()
	b = wxDateTime_UNow()
	if self.end_date.GetValue().Subtract(self.begin_date.GetValue()).IsEqualTo(wxDateSpan(days = 1)):
	    self.period.SetValue(0)
	elif self.end_date.GetValue().Subtract(self.begin_date.GetValue()).IsEqualTo(wxDateSpan(days = 7)):
	    self.period.SetValue(1)
	elif self.end_date.GetValue().Subtract(self.begin_date.GetValue()).IsEqualTo(wxDateSpan(months = 1)):
	    self.period.SetValue(2)
	elif self.end_date.GetValue().Subtract(self.begin_date.GetValue()).IsEqualTo(wxDateSpan(years = 1)):
	    self.period.SetValue(3)
	else: 
            self.period.SetValue(4)
        
    def OnChoosePeriod(self, event):
    	a = self.period.GetStringSelection()
	b = wxDateTime_UNow()
	if a == "Last Month":
	    self.end_date.SetValue(b)
	    self.begin_date.SetValue(b.SubtractDS(wxDateSpan_Month()))
	elif a == "Last Week":
	    self.end_date.SetValue(b)
	    self.begin_date.SetValue(b.SubtractDS(wxDateSpan_Days(7)))
	elif a == "Last Year":
	    self.end_date.SetValue(b)
	    self.begin_date.SetValue(b.SubtractDS(wxDateSpan_Year()))
	elif a == "Last Day":
	    self.end_date.SetValue(b)
	    self.begin_date.SetValue(b.SubtractDS(wxDateSpan_Day()))
	elif a == "Other":
            self.statusBar.SetStatusText(b)
	self.fichierText.SetValue(self.maker.fileManager.getFileName(self.script.GetStringSelection(), self.period.GetStringSelection(), [self.begin_date.GetValue().FormatISODate(), self.end_date.GetValue().FormatISODate()]))

    def OnSelectFile(self, event):
    	a = wxFileDialog(parent=self, message = "Save as", defaultDir = "", defaultFile = "rapport.pdf", wildcard = "*.pdf", style = wxSAVE)
	b = a.ShowModal()
	if b == wxID_OK:
	    self.fichierText.SetValue("%s/%s" % (a.GetDirectory(), a.GetFilename()))
	else:
	    self.fichierText = "Error"

    def OnChooseScript(self, event):
        a = self.script.GetStringSelection()
	try:
	    a = __import__("reports." + a)
	except:
            self.statusBar.SetStatusText("This script won't work")
	self.fichierText.SetValue(self.maker.fileManager.getFileName(self.script.GetStringSelection(), self.period.GetStringSelection(), [self.begin_date.GetValue().FormatISODate(), self.end_date.GetValue().FormatISODate()]))


    def OnCancel(self,event):
        if self.is_dialog:
            self.parent.close_the_window()
    
    def date2Date(self, date):
    	print "%d-%02d-%02d" % (date.GetYear(), date.GetMonth(), date.GetDay()) 
    	return "%d-%02d-%02d" % (date.GetYear(), date.GetMonth(), date.GetDay()) 
    
    def OnGenerateAndShow(self,event):
    	import os
	self.OnGenerate(event)
	print self.fichierText.GetValue()

    	os.spawnv(os.P_NOWAIT, cfg.get("pdf_open_program"), [cfg.get("pdf_open_program"), self.fichierText.GetValue()])	

    def OnGenerate(self,event):
    	from reports.PdfReport import fakeArgs
	from reports.SalesReport import SalesReport
	try:
	    a = SalesReport(args = fakeArgs(dict([('begin_date', self.date2Date(self.begin_date.GetValue()) ), ('end_date', self.date2Date(self.end_date.GetValue())), ("what", "%")])))
	except TypeError:
           dlg = wxMessageDialog(self, 'There is no sales on that period', style = wxICON_ERROR + wxCANCEL)
           dlg.ShowModal() 
	else:
	    filename = self.fichierText.GetValue()
	   
	    # TODO: make a complete test for a valid filename
	    if filename == "":
                dlg = wxMessageDialog(self, 'Invalid filename !', style = wxICON_ERROR + wxCANCEL)
                dlg.ShowModal() 
	    else:
	        a.pukePDF(self.fichierText.GetValue())

