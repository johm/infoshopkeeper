from Report import Report

from objects.kind import Kind
from objects.title import Title

class BestSellersReportWithDistributors(Report):
    metadata={'name':'Best Sellers Report With Distributors','action':'bestsellersreportwithdistributors'}
    do_total=False
    def query(self,args):
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
        select booktitle,count(book.id) as blah,publisher,title.id  from book,title where book.title_id=title.id and book.status='SOLD' and title.kind_id=%s group by title_id order by blah desc limit 500
        """,(args['kind']))
        results_pre_distributor= self.cursor.fetchall()
        self.cursor.close()
	results=[]
	for r in results_pre_distributor:
	    title=Title.get(r[3])
	    rl=list(r)
	    rl.append(title.distributors_as_string())
	    results.append(rl)	    

        return results

    def format_results(self,results):
        return ["<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0],r[1],r[2],r[4])  for r in results]


    def _queryForm(self):
        val="<select class='textbox' id='kind' name='kind'>"
        for k in list(Kind.select()):
            val = val+"<option value='%s'>%s</option>" % (k.id,k.kindName)
        val=val+"</select>"
        return val
