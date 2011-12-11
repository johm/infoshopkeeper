from SalesReport import SalesReport

class SalesReportByOwner(SalesReport):
    metadata={'name':'Sales Report by Owner','action':'salesreportowner'}
    total_index=1
    do_total=True
    
    def query(self,args):
        self.cursor=self.conn.cursor()
        begin_date=args.get('begin_date','1990-01-01')
        end_date=args.get('end_date','2030-01-01')
        owner=args.get('owner','')
        self.cursor.execute("SELECT * FROM transactionLog WHERE action='SALE' AND info LIKE %s AND date>=%s AND date<=ADDDATE(%s,INTERVAL 1 DAY) and owner=%s order by date" ,("%%%s%%" % (args['what']),begin_date,end_date,owner ))
        results= self.cursor.fetchall()
        self.cursor.close()
        return results

    def _queryForm(self):
        options=''
        self.cursor=self.conn.cursor()
        self.cursor.execute("SELECT distinct(owner) from transactionLog")
        results=self.cursor.fetchall()
        for r in [x[0] for x in results]:
            if r==self.args.get("owner","no owner"):
                options = options + "<OPTION SELECTED='true'>%s</OPTION" % (r)
            else:
                options = options + "<OPTION>%s</OPTION" % (r)

        self.cursor.close()
        
        
        return """<label class='textbox' for='owner'>Owner</label> <select class='textbox' name='owner' id='owner'/>%s</select><br />""" % (options) + SalesReport._queryForm(self)
