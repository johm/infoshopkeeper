from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from Report import Report
from PdfReport import PdfReport
from reportlab.lib.units import inch


class DailyReport(Report, PdfReport):
    metadata={'name':'Daily Report','action':'dailyreport'}
    reportname = 'Daily Report'
    total_index=1
    do_total=False
        
    def query(self,args):
        self.cursor=self.conn.cursor()

        begin_date=args.get('begin_date','1990-01-01')

	total_sales=0
	try:
            self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE action='SALE' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_sales = "%.2f" % self.cursor.fetchone()[0]
	except:
            pass
        
	total_cashout=0
        
	try:
            self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE action='CASH_REMOVED' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_cashout = "%.2f" % self.cursor.fetchone()[0]
        except:
            pass


	total_deposits=0
        
	try:
            self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE action='DEPOSIT' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_deposits = "%.2f" % self.cursor.fetchone()[0]
        except:
            pass


        total_taxes=0
        try:
            self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE action='TAX' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_taxes = "%.2f" % self.cursor.fetchone()[0]
	except:
            pass
            
            
        begin_drawer=0
        try:
            self.cursor.execute("SELECT amount FROM cashbox WHERE date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date asc limit 1" ,(begin_date,begin_date))
            begin_drawer = "%.2f" % self.cursor.fetchone()[0]

        except:
            pass
        
            
        end_drawer=0
        try:
            self.cursor.execute("SELECT amount FROM cashbox WHERE date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date desc limit 1" ,(begin_date,begin_date))
            end_drawer = "%.2f" % self.cursor.fetchone()[0]
        except:
            pass

        
	self.cursor.execute("SELECT amount,action,cashier FROM transactionLog WHERE (action='OPEN_PRECOUNT' or action='OPEN_POSTCOUNT') AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
        drawer_counts=self.cursor.fetchall()
	counts=[]
	for c in drawer_counts:
            counts.append(("%s:%s" % (c[1], c[2]),"%.2f" % c[0]))
	


        total_cash=0
	total_check=0
	total_credit=0
        
	try:
	    self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE (action='SALE' or action='TAX') AND paid_how='cash' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_cash = "%.2f" % self.cursor.fetchone()[0]
	except:
	    pass

	try:
   	    self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE (action='SALE' or action='TAX') AND paid_how='check' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_check = "%.2f" % self.cursor.fetchone()[0]
	except:
	    pass


	try:
	    self.cursor.execute("SELECT sum(amount) FROM transactionLog WHERE (action='SALE' or action='TAX') AND paid_how='credit' AND date>=%s  AND date<=ADDDATE(%s,INTERVAL 1 DAY) order by date " ,(begin_date,begin_date))
            total_credit = "%.2f" % self.cursor.fetchone()[0]
	except:
	    pass



	


	results = [("Date",begin_date),
		   ("Total Sales",total_sales),
		   ("Sales Tax Collected",total_taxes),
		   ("Cash In",total_cash),
		   ("Credit Total",total_credit),
		   ("Checks Total",total_check),
		   ("Cash Out",total_cashout),
                   ("Cash Deposits",total_deposits),
		   ("Start Drawer(projected)",begin_drawer),
		   ("End Drawer(projected)",end_drawer)]+counts
        self.cursor.close()
        return results
    
    def format_results(self,results):
	print results
        return ["<tr><td>%s</td><td>%s</td></tr>" % (r[0],r[1])  for r in results]

    def format_results_as_pdf(self,results):
        self.defineConstants()
	if len(results) == 0:
	    raise TypeError
	num_rows = len(results) 
	rows_height = []  
	for a in range(num_rows):
		rows_height.append(None)
	colwidths = ( None,None,None,None,None,None,None,None)
	
	
	print results
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
        return """<label class='textbox' for='begin_date'>Date</label><input type='text' class='textbox' name='begin_date' id='begin_date' value='%s'/>

        <script type='text/javascript'>
        Calendar.setup({
        inputField     :    'begin_date',   // id of the input field
        ifFormat       :    '%%Y-%%m-%%d',       // format of the input field
        showsTime      :    false,
    });
        </script>
        """ % (self.args.get("begin_date",""))

