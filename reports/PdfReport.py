#!/usr/bin/python
# Copyright 2007 Guillaume Beaulieu

# Parts of this code is ripped off from online tutorial from
# http://wiki.w4py.org/pdf-creation-with-reportlab.html on the
# 10 February 2007. There were no information about copyright on
# wiki, but since the code will soon be unrecognizable, and 
# wiki almost require non restrictive license on post, I guess
# this is "fair use".

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

from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from time import *
import datetime
from wxPython.wx import *
from os import *
from infoshopkeeper_config import configuration
cfg = configuration()
addr = cfg.get("infoshopaddress")
name = cfg.get("infoshopname")

dirAssociations = {
"Last Day": "daily",
"Last Week": "weekly",
"Last Month": "monthly",
"Last Year": "yearly",
"Other": "others",
}
 
class PdfReportDirectoryManager:
# this class is creating a Manager for the reports. Since all the
# reports will often be done monthly or something like that, it
# would be rad to have them in different directories, and if possible
# auto selected and everything
    def __init__(self): 
        if not access(cfg.get("reports_directory"), F_OK|R_OK|W_OK):
           dlg = wxMessageDialog(self, 'Can\'t read write the etc.py defined reports_directory')
           dlg.ShowModal() 
	   return
	self.directory = cfg.get("reports_directory")
	     

    def getFileName(self,reportType, timing, dates = []):
    	thoseReportsDirectory = path.join(self.directory, reportType )
        if not access(thoseReportsDirectory, F_OK):
	    print "creating " + thoseReportsDirectory + "..."
	    mkdir(thoseReportsDirectory)
	thoseTimelyReportsDirectory = path.join(thoseReportsDirectory, dirAssociations[timing] ) 
        if not access(thoseTimelyReportsDirectory, F_OK):
	    print "creating " + thoseTimelyReportsDirectory + "..."
	    mkdir(thoseTimelyReportsDirectory)
	if dirAssociations[timing] == "daily":
            filename = str(datetime.date.today()) + ".pdf"
	elif dirAssociations[timing] == "weekly":
	    filename = "week" + str(wxDateTime.Now().GetWeekOfYear()) + "of" +  str(wxDateTime.Now().GetYear()) + ".pdf"
	elif dirAssociations[timing] == "monthly":
	    filename = str(wxDateTime.Now().GetMonth()) + "of" +  str(wxDateTime.Now().GetYear()) + ".pdf"
	elif dirAssociations[timing] == "yearly":
	    filename = "year" + str(wxDateTime.Now().GetYear()) + ".pdf"
	else:
	    print dates
	    filename = "from" + dates[0] + "to" + dates[1] + ".pdf" 
	return path.join(thoseTimelyReportsDirectory, filename)

        
        
       

class fakeArgs:
    # this is a class that fake the args for the sales report module
    def __init__(self, args):
	self.values = args

    def __getitem__(self, kekchose):
	return self.get(kekchose, "")
		
    def get(self, arg1, arg2):
    	if self.values.has_key(arg1):
	    return self.values[arg1]
	else:
	    return arg2
        

class PdfReport:

    def __init__(self):
        self.fileManager = PdfReportDirectoryManager()

    def defineConstants(self):
        self.PAGE_HEIGHT = letter[1]
	self.PAGE_WIDTH = letter[0]
    	
    def makePresentationPage( self, canvas, doc):
        canvas.saveState()
        canvas.setFont( 'Times-Bold', 16 )
        canvas.drawCentredString( self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-( 0.25*inch ), unicode(name) )
        canvas.line( 0.5*inch, self.PAGE_HEIGHT-( 0.35*inch ), self.PAGE_WIDTH-( 0.5*inch ), self.PAGE_HEIGHT-( 0.35*inch ) )
        canvas.setFont( 'Times-Bold', 8 )
        canvas.drawCentredString( self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-( 0.45*inch ), unicode(addr) )
        canvas.saveState()
        canvas.setFont( 'Times-Bold', 16 )
        canvas.drawCentredString( self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-( 1*inch ), unicode(self.reportname) )
	

    def addPagenum( self, canvas, doc ):
        canvas.saveState()
        # Header
        canvas.setFont( 'Times-Roman', 9 )
        canvas.drawString( 0.5*inch, self.PAGE_HEIGHT-( 0.5*inch ), 'Page %d' % doc.page )
        canvas.drawRightString( self.PAGE_WIDTH-( 0.5*inch ), self.PAGE_HEIGHT-( 0.5*inch ), theDate )
        # Footer.
        canvas.drawString( inch, 0.5*inch, 'Page %d' % ( doc.page ) )
        canvas.restoreState()

    def pukePDF( self , filename):
        # Generate the PDF
	doc = SimpleDocTemplate( filename, pagesize = letter, leftMargin = 0.5*inch, rightMargin = 0.5*inch, bottomMargin = 1.5*inch )
        Story = [ Spacer( 1, 0.15*inch ) ]
        # Get the flowable from the report python
        table = self.format_results_as_pdf(self.query(self.args))
        Story.append( table )
        Story.append( Spacer( 1, 0.15*inch ) )
        doc.build( Story, onFirstPage=self.makePresentationPage, onLaterPages=self.addPagenum )


