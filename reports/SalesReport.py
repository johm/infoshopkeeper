from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from Report import Report
import sys
import codecs
from PdfReport import PdfReport
from reportlab.lib.units import inch


class SalesReport(Report, PdfReport):
    metadata={'name':'Sales Report','action':'salesreport'}
    reportname = 'Sales Report'
    total_index=1
    do_total=True
        
    def query(self,args):
        self.cursor=self.conn.cursor()
        begin_date=args.get('begin_date','1990-01-01')
        end_date=args.get('end_date','2030-01-01')
        self.cursor.execute("SELECT * FROM transactionLog WHERE action='SALE' AND info LIKE %s AND date>=%s AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date" ,("%%%s%%" % (args['what']),begin_date,end_date ))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results
    
    def format_results(self,results):
        return ["<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[2],r[4],r[1])  for r in results]

    def workResults(self, results):
    	count = 0
	newtable = list()
	countRow = 0
        for a in results:
	    newtable.append(list())
	    countCol = 0
	    for b in a:
	        if b == None:
		    newtable[countRow].append(" ")
		else:    
	    	    if (countCol == 0 or countCol == 1 or countCol == 2 or countCol == 3 or countCol == 6 or countCol == 8):
		        newtable[countRow].append(b)
		    else:
			#newtable[countRow].append( unicode( b.decode("string_escape").encode("utf8", "strict"), "utf8") ) 
			#newtable[countRow].append( unicode(b, "string_escape", "strict") ) 
			#newtable[countRow].append( unicode( b.decode("string_escape").encode("latin-1", "strict"), "latin1") ) 
			patente = b.decode("unicode_escape")
			newtable[countRow].append( patente ) 
		countCol += 1
	    countRow += 1
	return newtable
	
    def format_results_as_pdf(self,results):
        self.defineConstants()
	if len(results) == 0:
           dlg = wxMessageDialog(self, 'There are no data in the selected set (maybe you have the wrong dates ?)')
           dlg.ShowModal() 
	   return
	
	num_rows = len(results) 
	rows_height = []  
	for a in range(num_rows):
		rows_height.append(None)
	colwidths = ( None,None,None,None,None,None,None,None)
	print results
	results = self.workResults(results)
	t = Table( results )
	#t = Table( results, colwidths, rows_height )
        GRID_STYLE = TableStyle(
        [     ('GRID', (0,0), (-1,-1), 0.25, colors.black),
              ('FONT', (0,-1), (-1, -1), "Times-Bold"),
#              ('FONT', (0,1), (-1, -1), "Times-Roman"),
	      ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
        )
        t.setStyle( GRID_STYLE )
	return t

     
    def _queryForm(self):
        return """<label class='textbox' for='what'>What</label> <input type='text' class='textbox' name='what' id='what' value='%s'/>
        <label class='textbox' for='begin_date'>Begin Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/>
        <label class='textbox' for='end_date'>End Date</label><input type='text' class='textbox' name='end_date' id='end_date' value='%s'/>
        <script type='text/javascript'>
        Calendar.setup({
        inputField     :    'begin_date',   // id of the input field
        ifFormat       :    '%%Y-%%m-%%d',       // format of the input field
        showsTime      :    false,
    });
    Calendar.setup({
        inputField     :    'end_date',   // id of the input field
        ifFormat       :    '%%Y-%%m-%%d',       // format of the input field
        showsTime      :    false,
    });
        </script>
        """ % (self.args.get("what",""),self.args.get("begin_date",""),self.args.get("end_date",""))

