# a base class for all reports
from components import db
from formencode import htmlfill


class Report:
    total_index=0
    do_total=True
    
    def __init__(self,args):
        self.conn=db.connect()
        self.args=args

    def get_total(self,results):
        total=0
        for r in results:
            total=total+r[self.total_index]
        return total
        
    def query(self,args):
        self.cursor=self.conn.cursor()
    
    def queryForm(self):
        top="<form action='/report' method='get'>"
        bottom_template="<input type='hidden' name='query_made' value='yes'/><input type='hidden' name='reportname'/><input type='submit' class='submit' value='get report'/></form>"
        defaults={"query_made":"yes","reportname":self.metadata['action']}
        parser=htmlfill.FillingParser(defaults)
        parser.feed(bottom_template)
        parser.close()
        html=top+self._queryForm()+parser.text()
        return html

    def _queryForm(self):
        return ""
